from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        read_only_fields = ['id'] # Make these fields read-only if needed

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Ensure password is write-only

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} # Ensure password is write-only

    def create(self, validated_data):
        password = validated_data.pop('password', None) # Extract password
        instance = self.Meta.model(**validated_data) # Create user instance
        if password is not None:
            instance.set_password(password) # Hash the password
        instance.save()
        return instance