from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import *
from listings.serializers import GuideProfileSerializer, HotelProfileSerializer
from listings.models import GuideProfile, HotelProfile

class RegisterView(generics.CreateAPIView):
    # createAPIView recives the request, creates a serializer instance with the request data, validates it, and calls the create() method if valid
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # AllowAny means that any user (authenticated or not) can access this view, which is appropriate for registration endpoints

def getprofile(user):
        if(user.role=='traveler'):
            profile = TravelerProfile.objects.get_or_create(user = user)[0]
        if(user.role=='guide'):
            profile = GuideProfile.objects.get_or_create(user = user)[0]
        if(user.role=='hotel'):
            profile = HotelProfile.objects.get_or_create(user = user)[0]
        
        return profile

class MeView(APIView): # APIView is a more flexible view that allows us to define custom behavior for different HTTP methods (GET, POST, PATCH, etc.)
    permission_classes = [IsAuthenticated]

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