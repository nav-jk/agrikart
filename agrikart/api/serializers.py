from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_farmer', 'is_buyer']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ✅ Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_farmer'] = user.is_farmer
        token['is_buyer'] = user.is_buyer
        token['phone'] = user.phone_number

        return token
