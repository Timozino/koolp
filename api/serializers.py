
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from userAuth.models import CustomUser, Profile



from userAuth import models as api_models



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = '__all__'
        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        

  
            
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "fullName", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists!"})

        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists!"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from validated_data
        user = CustomUser.objects.create_user(**validated_data)
        return user
            
            
            



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.CustomUser
        fields = '__all__'


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Profile
        fields = '__all__'