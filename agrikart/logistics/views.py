from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from buyer.models import Order
from farmer.models import Farmer
from .models import LogisticsPartner
from .utils import haversine
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import viewsets
from logistics.models import CourierAssignment
from logistics.serializers import CourierAssignmentSerializer
from rest_framework.permissions import IsAuthenticated
from buyer.serializers import OrderSerializer
from .utils import generate_order_pdf
from django.http import FileResponse
from buyer.models import Order



class NearbyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_logistics:
            return Response({"detail": "Not authorized"}, status=403)

        logistics = LogisticsPartner.objects.get(user=user)
        logistics_lat = logistics.latitude
        logistics_lon = logistics.longitude

        confirmed_orders = Order.objects.filter(status='CONFIRMED').prefetch_related('items__produce')
        nearby_orders = []

        for order in confirmed_orders:
            try:
                cart_items = order.items.all()
                first_item = cart_items[0] if cart_items else None
                if not first_item:
                    continue

                farmer = first_item.produce.farmer
                if farmer.latitude is None or farmer.longitude is None:
                    continue

                dist = haversine(logistics_lon, logistics_lat, farmer.longitude, farmer.latitude)

                if dist <= 15:
                    nearby_orders.append({
                        "order_id": order.id,
                        "status": order.status,
                        "buyer_address": order.buyer.address,
                        "farmer_name": farmer.name,
                        "farmer_address": farmer.address,
                        "farmer_lat": farmer.latitude,
                        "farmer_lon": farmer.longitude,
                        "distance_km": round(dist, 2),
                        "items": [
                            {
                                "produce": {
                                    "name": item.produce.name
                                },
                                "quantity": item.quantity
                            } for item in cart_items
                        ]
                    })

            except Exception as e:
                print(f"❌ Error processing order {order.id}: {e}")
                continue

        return Response(nearby_orders, status=status.HTTP_200_OK)



class CourierAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CourierAssignment.objects.all()
    serializer_class = CourierAssignmentSerializer
    permission_classes = [IsAuthenticated]




class AssignedOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_logistics:
            return Response({"detail": "Not authorized"}, status=403)

        assignments = CourierAssignment.objects.filter(courier__user=user).select_related('order')
        orders = [assignment.order for assignment in assignments]
        return Response(OrderSerializer(orders, many=True).data)


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        valid_statuses = dict(Order.STATUS_CHOICES).keys()

        if new_status not in valid_statuses:
            return Response({"error": f"Invalid status. Allowed: {list(valid_statuses)}"}, status=400)

        order.status = new_status
        order.save()
        return Response({"message": f"Order status updated to {new_status}"}, status=200)
    


class OrderReceiptPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        if not request.user.is_logistics:
            return Response({"error": "Unauthorized"}, status=403)

        pdf_buffer = generate_order_pdf(order)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"Order_{order_id}_receipt.pdf")
