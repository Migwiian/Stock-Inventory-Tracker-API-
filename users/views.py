from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import UserSerializer, UserRegistrationSerializer
# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    '''This API view allows new users to register.
    The API endpoint is open to all users.
    The view uses the UserRegistrationSerializer to validate and create new users.
    Authentication is not required to access this endpoint.'''
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] 

class UserDetailView(generics.RetrieveAPIView):
    '''This API view allows authenticated users to retrieve their own user details.
    The API endpoint is restricted to authenticated users only.
    The view uses the UserSerializer to serialize the user data.
    Authentication is handled via JWT tokens.'''
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override get_object to return the authenticated user
    def get_object(self):
        return self.request.user 

class UserProfileView(generics.RetrieveUpdateAPIView):
    '''This API view allows authenticated users to retrieve and update their own profile information.
    The API endpoint is restricted to authenticated users only.
    The view uses the UserSerializer to serialize and update the user data.
    Authentication is handled via JWT tokens.'''
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override get_object to return the authenticated user
    def get_object(self):
        return self.request.user
