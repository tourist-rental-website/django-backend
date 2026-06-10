from jsonschema import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import GuideProfile, HotelProfile, Package, Room
from .serializers import GuideProfileSerializer, HotelProfileSerializer, PackageSerializer, RoomSerializer


class GuideProfileCreateView(generics.CreateAPIView):
    serializer_class = GuideProfileSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a guide profile

    def perform_create(self, serializer): 
        if self.request.user.role != 'guide': # Check if the authenticated user has the role of 'guide'
            raise ValidationError("Only guide users can create a guide profile.")
        serializer.save(user=self.request.user)

class GuideProfileListView(generics.ListAPIView):
    queryset = GuideProfile.objects.all()
    serializer_class = GuideProfileSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of guides

class HotelProfileCreateView(generics.CreateAPIView):
    serializer_class = HotelProfileSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a hotel profile

    def perform_create(self, serializer): 
        if self.request.user.role != 'hotel': # Check if the authenticated user has the role of 'hotel'
            raise ValidationError("Only hotel users can create a hotel profile.")
        serializer.save(user=self.request.user)

class HotelProfileListView(generics.ListAPIView):
    queryset = HotelProfile.objects.all()
    serializer_class = HotelProfileSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of hotels

class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a room

    def perform_create(self, serializer):
        if self.request.user.role != 'hotel': # Check if the authenticated user has the role of 'hotel'
            raise ValidationError("Only hotel users can create rooms.")
        hotel_profile = self.request.user.hotel_profile
        serializer.save(hotel=hotel_profile)

class RoomListView(generics.ListAPIView):
    get_queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of rooms

class PackageCreateView(generics.CreateAPIView):
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a package

    def perform_create(self, serializer):
        if self.request.user.role != 'guide': # Check if the authenticated user has the role of 'guide'
            raise ValidationError("Only guide users can create packages.")
        guide_profile = self.request.user.guide_profile
        serializer.save(guide=guide_profile)

class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of packages