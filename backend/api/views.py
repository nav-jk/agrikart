from rest_framework import viewsets
from farmer.models import Farmer
from buyer.models import Buyer
from .serializers import FarmerSerializer, BuyerSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import SignupSerializer
from .serializers import FarmerSignupSerializer
from buyer.models import CartItem, Order, Buyer
from farmer.models import Produce
from .serializers import CartItemSerializer, OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from buyer.models import CartItem
from .serializers import CartItemSerializer
from rest_framework.permissions import IsAuthenticated


class FarmerViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone_number'
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer

class BuyerViewSet(viewsets.ModelViewSet):
    lookup_field = 'phone_number'
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def farmer_signup_view(request):
    serializer = FarmerSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Farmer account created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    try:
        buyer = user.buyer_profile
    except:
        return Response({"error": "User is not a buyer"}, status=400)

    produce_id = request.data.get('produce')
    quantity = request.data.get('quantity')

    if not produce_id or not quantity:
        return Response({"error": "produce and quantity are required"}, status=400)

    try:
        produce = Produce.objects.get(id=produce_id)
    except Produce.DoesNotExist:
        return Response({"error": "Produce not found"}, status=404)

    cart_item = CartItem.objects.create(buyer=buyer, produce=produce, quantity=quantity)
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_from_cart(request):
    user = request.user
    try:
        buyer = user.buyer_profile
    except:
        return Response({"error": "User is not a buyer"}, status=400)

    # Check for unconfirmed orders
    if Order.objects.filter(buyer=buyer, status='PENDING').exists():
        return Response({"error": "You have a pending order. Confirm payment first."}, status=400)

    cart_items = CartItem.objects.filter(buyer=buyer)
    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    order = Order.objects.create(buyer=buyer)
    order.items.set(cart_items)
    order.save()

    # Clear cart after creating order
    cart_items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=201)



class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit access to own cart items
        return self.queryset.filter(buyer__user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order_payment(request, order_id):
    user = request.user
    try:
        order = Order.objects.get(id=order_id, buyer__user=user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    if order.status != 'PENDING':
        return Response({"error": "Order is not pending or already confirmed."}, status=400)

    order.status = 'CONFIRMED'
    order.save()
    return Response({"message": "Payment confirmed. Order status updated."}, status=200)
