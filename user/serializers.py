from .models import User
from wallet.models import Wallet
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data['password']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user_wallet = Wallet.objects.create(user=user)
        if user_wallet:
            user_wallet.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("Email is required")
        if not password:
            raise serializers.ValidationError("Password is required")
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
        

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"\
        

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)