from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import *
from listings.serializers import GuideProfileSerializer, HotelProfileSerializer
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from listings.models import  GuideProfile, HotelProfile
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Save the user
        user = serializer.save()

        # Create corresponding profile
        getprofile(user)

        # Generate verification token and encoded user id
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Build verification URL
        verification_url = (
            f"http://127.0.0.1:8000/accounts/verify/{uid}/{token}/"  
        )
        
#        # use this to redirect in react app - this is reacts url
#        verification_url = (
#            f"http://localhost:5173/verify-email/{uid}/{token}/"
#        )

        # Send verification email
        send_mail(
            subject="Verify your Email",
            message=(
                f"Hi {user.first_name},\n\n"
                f"Click the link below to verify your email:\n\n"
                f"{verification_url}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        
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

def getprofile(user):
    if user.role == "traveler":
        profile = TravelerProfile.objects.get_or_create(user=user)[0]

    elif user.role == "guide":
        profile = GuideProfile.objects.get_or_create(user=user)[0]

    elif user.role == "hotel":
        profile = HotelProfile.objects.get_or_create(user=user)[0]

    return profile

class MeView(APIView): # APIView is a more flexible view that allows us to define custom behavior for different HTTP methods (GET, POST, PATCH, etc.)
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # allows multipart/form-data requests (file uploads)

    def get(self, request): # This method will be called when a GET request is made to the /me/ endpoint
        profile = getprofile(request.user)
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