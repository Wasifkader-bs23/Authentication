from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password','is_verified']
        extra_kwargs = {
            'is_verified': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp = serializers.CharField()
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['email' , 'password']

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name','email']

class ResetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
        