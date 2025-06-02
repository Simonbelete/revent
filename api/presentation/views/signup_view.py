from rest_framework import generics
from rest_framework.permissions import AllowAny

from presentation import serializers

class SignupViewSet(generics.CreateAPIView):
    serializer_class = serializers.SignupSerializer
    permission_classes = [AllowAny]