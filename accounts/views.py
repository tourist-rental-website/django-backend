from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    # createAPIView recives the request, creates a serializer instance with the request data, validates it, and calls the create() method if valid
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # AllowAny means that any user (authenticated or not) can access this view, which is appropriate for registration endpoints