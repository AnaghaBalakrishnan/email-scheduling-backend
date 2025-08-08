# users/serializers.py
from rest_framework import serializers
from .models import User
from django.utils import timezone

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile_picture') # Fields for registration [cite: 17]

    def create(self, validated_data):
        # Create a user but set them as inactive until verified
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture'),
            is_active=False # User cannot log in until verified
        )
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_picture',)