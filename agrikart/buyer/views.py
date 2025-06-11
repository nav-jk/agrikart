from rest_framework import viewsets
from .models import CartItem, Order, Buyer
from .serializers import CartItemSerializer, OrderSerializer, BuyerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics

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
        items = CartItem.objects.filter(buyer=buyer)
        if not items:
            return Response({"error": "Cart empty"}, status=400)
        order = Order.objects.create(buyer=buyer)
        order.items.set(items)
        items.delete()
        return Response(OrderSerializer(order).data)

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
