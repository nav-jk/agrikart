from rest_framework import viewsets
from .models import CartItem, Order, Buyer
from .serializers import CartItemSerializer, OrderSerializer, BuyerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics
import requests
from decimal import Decimal
from collections import defaultdict
from django.db import transaction
from .utils import generate_random_lat_lon
from logistics.models import CourierAssignment
from logistics.utils import generate_order_pdf
from django.http import FileResponse

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(buyer__user=self.request.user)

    def perform_create(self, serializer):
        buyer = Buyer.objects.get(user=self.request.user)
        serializer.save(buyer=buyer)


class CreateOrderFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        buyer = Buyer.objects.get(user=request.user)
        print(f"🧾 Buyer: {buyer}")
        items = CartItem.objects.select_related('produce').filter(buyer=buyer)
        print(f"🛒 Cart Items: {[str(i) for i in items]}")

        if not items:
            print("❌ Cart is empty")
            return Response({"error": "Cart empty"}, status=400)

        with transaction.atomic():
            notify_data = {}

            for item in items:
                produce = item.produce
                print(f"🌽 Checking produce: {produce.name}, stock={produce.quantity}, requested={item.quantity}")
                if produce.quantity < item.quantity:
                    print("❌ Insufficient stock")
                    return Response({
                        "error": f"Insufficient stock for {produce.name} (Available: {produce.quantity}, Requested: {item.quantity})"
                    }, status=400)

                produce.quantity -= item.quantity
                if produce.quantity <= 0:
                    produce.is_active = False
                produce.save()

                farmer_phone = produce.farmer.user.phone_number
                if farmer_phone not in notify_data:
                    notify_data[farmer_phone] = []
                notify_data[farmer_phone].append({
                    "produce": produce.name,
                    "quantity_bought": float(item.quantity),
                    "remaining_stock": float(produce.quantity)
                })

            print("✅ Creating order...")
            order = Order.objects.create(
                buyer=buyer,
                buyer_lat=buyer.latitude,
                buyer_lon=buyer.longitude
            )
            order.items.set(items)

            farmer = items[0].produce.farmer
            print(f"🌍 Farmer: {farmer.name}, lat={farmer.latitude}, lon={farmer.longitude}")

            if not farmer.latitude or not farmer.longitude:
                print("❌ Order missing farmer coordinates")
            else:
                order.farmer_lat = farmer.latitude
                order.farmer_lon = farmer.longitude

            order.save()

            from logistics.utils import assign_order_to_courier
            assign_order_to_courier(order)

        for farmer_phone, produce_list in notify_data.items():
            self.notify_farmer_on_order(farmer_phone, produce_list)

        print("✅ Order created successfully")
        return Response(OrderSerializer(order).data)


    def notify_farmer_on_order(self, farmer_phone, items):
        buyer = self.request.user.buyer
        order = Order.objects.filter(buyer=buyer).latest('id')

        # 🛵 Get courier name for this order
        courier_assignment = CourierAssignment.objects.filter(order=order).first()
        courier_name = courier_assignment.courier.name if courier_assignment else "Unknown"

        payload = {
            "phone_number": farmer_phone,
            "items": items,
            "order_id": order.id,
            "buyer_address": buyer.address,
            "courier": courier_name
        }

        try:
            print(f"📡 Notifying farmer {farmer_phone} with items: {items}")
            requests.post("http://localhost:5000/notify-farmer", json=payload)
        except Exception as e:
            print(f"❌ Failed to notify farmer {farmer_phone}: {e}")



class ConfirmOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, buyer__user=request.user)
            order.status = 'CONFIRMED'
            order.save()
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class BuyerDetailUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, phone_number):
        buyer = get_object_or_404(Buyer, user__phone_number=phone_number)
        return Response(BuyerSerializer(buyer).data)

    def put(self, request, phone_number):
        buyer = get_object_or_404(Buyer, user__phone_number=phone_number)
        serializer = BuyerSerializer(buyer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, phone_number):
        buyer = get_object_or_404(Buyer, user__phone_number=phone_number)
        buyer.delete()
        return Response(status=204)





class BuyerListCreateView(generics.ListCreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lat, lon = generate_random_lat_lon()
        serializer.save(latitude=lat, longitude=lon)


class ConfirmOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, buyer__user=request.user)
            order.status = 'CONFIRMED'
            order.save()
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


class BuyerDetailUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, phone_number):
        buyer = get_object_or_404(Buyer, user__phone_number=phone_number)
        return Response(BuyerSerializer(buyer).data)

    def put(self, request, phone_number):
        buyer = get_object_or_404(Buyer, user__phone_number=phone_number)
        serializer = BuyerSerializer(buyer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, phone_number):
        buyer = get_object_or_404(Buyer, user__phone_number=phone_number)
        buyer.delete()
        return Response(status=204)



class BuyerListCreateView(generics.ListCreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = [IsAuthenticated]


class OrderReceiptDownload(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        # Permission check (optional for security)
        if request.user != order.buyer.user:
            return Response({"detail": "Not allowed"}, status=403)

        buffer = generate_order_pdf(order)
        return FileResponse(buffer, as_attachment=True, filename=f"order_{pk}_receipt.pdf")

# orders/views.py or buyer/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from buyer.models import Order
from logistics.utils import generate_order_pdf

class OrderReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404("Order not found")

        if request.user != order.buyer.user and not request.user.is_staff:
            return Response({"detail": "Not authorized to view this receipt."}, status=403)

        pdf_buffer = generate_order_pdf(order)
        return FileResponse(pdf_buffer, content_type='application/pdf')
