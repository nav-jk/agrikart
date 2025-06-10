from rest_framework import serializers
from farmer.models import Farmer, Produce
from buyer.models import Buyer, CartItem, Order
from django.contrib.auth.models import User
from rest_framework import serializers


class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'

class FarmerSerializer(serializers.ModelSerializer):
    produce = ProduceSerializer(many=True, read_only=True)

    class Meta:
        model = Farmer
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Buyer
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    phone_number = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'address']

    def create(self, validated_data):
        phone = validated_data.pop('phone_number')
        address = validated_data.pop('address')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        Buyer.objects.create(user=user, phone_number=phone, address=address)
        return user
