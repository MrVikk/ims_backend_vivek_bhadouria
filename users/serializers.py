# serializers.py
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            # Don't return the password in responses
            'password': {'write_only': True}  
        }
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value    

    def create(self, validated_data):
        # Hash the password when creating the user
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.password = make_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            return user
        else:
            raise serializers.ValidationError("Invalid email or password.")