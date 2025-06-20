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

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(buyer__user=self.request.user)

    def perform_create(self, serializer):
        buyer = Buyer.objects.get(user=self.request.user)
        serializer.save(buyer=buyer)



from django.db import transaction
from decimal import Decimal

class CreateOrderFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        buyer = Buyer.objects.get(user=request.user)
        items = CartItem.objects.select_related('produce').filter(buyer=buyer)

        if not items:
            return Response({"error": "Cart empty"}, status=400)

        with transaction.atomic():
            notify_data = {}

            for item in items:
                produce = item.produce
                if produce.quantity < item.quantity:
                    return Response({
                        "error": f"Insufficient stock for {produce.name} (Available: {produce.quantity}, Requested: {item.quantity})"
                    }, status=400)

                # 📉 Deduct stock
                produce.quantity -= item.quantity

                # ❌ Auto-disable if no stock
                if produce.quantity <= 0:
                    produce.is_active = False

                produce.save()

                # 📬 Prepare notification per farmer
                farmer_phone = produce.farmer.user.phone_number
                if farmer_phone not in notify_data:
                    notify_data[farmer_phone] = []
                notify_data[farmer_phone].append({
                    "produce": produce.name,
                    "quantity_bought": float(item.quantity),
                    "remaining_stock": float(produce.quantity)
                })

            order = Order.objects.create(buyer=buyer)
            order.items.set(items)
            items.delete()

        # 🔔 Notify farmers outside transaction
        for farmer_phone, produce_list in notify_data.items():
            self.notify_farmer_on_order(farmer_phone, produce_list)

        return Response(OrderSerializer(order).data)

    def notify_farmer_on_order(self, farmer_phone, items):
        payload = {
            "phone_number": farmer_phone,
            "items": items
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
