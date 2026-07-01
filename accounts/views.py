import token

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import *
from listings.serializers import GuideProfileSerializer, HotelProfileSerializer, ResetPasswordSerializer
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from listings.models import  GuideProfile, HotelProfile
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .services import create_user_profile, send_password_reset_email, send_verification_email
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        create_user_profile(user)

        send_verification_email(user)

class VerifyEmailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):

            return Response(
                {"message": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):

            user.is_verified = True
            user.save()

            return Response(
                {"message": "Email verified successfully."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Verification link is invalid or expired."},
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GoogleOAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_token = serializer.validated_data.get("id_token")

        if not settings.GOOGLE_CLIENT_ID:
            return Response(
                {"detail": "Google OAuth client ID is not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            id_info = google_id_token.verify_oauth2_token(
                id_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError:
            return Response(
                {"detail": "Invalid Google ID token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = id_info.get("email")
        email_verified = id_info.get("email_verified", False)

        if not email or not email_verified:
            return Response(
                {"detail": "Google account email must be verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": id_info.get("given_name", ""),
                "last_name": id_info.get("family_name", ""),
                "is_verified": True,
                "role": "traveler",
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        if not user.is_verified:
            user.is_verified = True
            user.save()

        create_user_profile(user)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"message": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        send_password_reset_email(user)

        return Response(
        {"message": "Password reset email sent successfully."},
        status=status.HTTP_200_OK,
        )
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"message": "Invalid password reset link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"message": "Password reset link is invalid or expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )

class MeView(APIView): # APIView is a more flexible view that allows us to define custom behavior for different HTTP methods (GET, POST, PATCH, etc.)
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # allows multipart/form-data requests (file uploads)

    def get(self, request): # This method will be called when a GET request is made to the /me/ endpoint
        profile = create_user_profile(request.user)

        if(request.user.role =='traveler'):
            serializer = TravelerProfileSerializer(profile)
        
        elif(request.user.role=='guide'):
            serializer = GuideProfileSerializer(profile)
        
        elif(request.user.role=='hotel'):
            serializer = HotelProfileSerializer(profile)
        
        return Response(serializer.data)

    def patch(self, request):
        user = request.user

        if user.role == "guide":
            serializer = GuideProfileSerializer(
                user.guide_profile,
                data=request.data,
                partial=True
            )

        elif user.role == "hotel":
            serializer = HotelProfileSerializer(
                user.hotel_profile,
                data=request.data,
                partial=True
            )

        elif user.role == "traveler":
            serializer = TravelerProfileSerializer(
                user.traveler_profile,
                data=request.data,
                partial=True
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)