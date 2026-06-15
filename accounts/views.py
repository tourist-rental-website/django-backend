from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import RegisterSerializer
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    # createAPIView recives the request, creates a serializer instance with the request data, validates it, and calls the create() method if valid
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # AllowAny means that any user (authenticated or not) can access this view, which is appropriate for registration endpoints

class MeView(APIView): # APIView is a more flexible view that allows us to define custom behavior for different HTTP methods (GET, POST, PATCH, etc.)
    permission_classes = [IsAuthenticated]

    def get(self, request): # This method will be called when a GET request is made to the /me/ endpoint
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request): # This method will be called when a PATCH request is made to the /me/ endpoint, allowing users to update their own information
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True  # IMPORTANT-partial=True allows for partial updates, meaning that users can update only a subset of their information without needing to provide all fields
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)