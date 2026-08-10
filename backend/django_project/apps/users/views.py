from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/user/profile/ — Returns the authenticated user's profile.
    PATCH /api/user/profile/ — Updates allowed profile fields.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Fixed: was AllowAny

    def get_object(self):
        return self.request.user
