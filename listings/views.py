from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import GuideProfile, HotelProfile, Room, Package
from .serializers import GuideProfileSerializer, HotelProfileSerializer, RoomSerializer, PackageSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class GuideProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = GuideProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # allows multipart/form-data requests (file uploads like images + normal form fields)

    def get_object(self):
        user = self.request.user

        if user.role != "guide":
            raise ValidationError("Only guide users can access guide profile.")

        return user.guide_profile

class GuideProfileListView(generics.ListAPIView):
    queryset = GuideProfile.objects.all()
    serializer_class = GuideProfileSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of guides

class HotelProfileUpadateView(generics.RetrieveUpdateAPIView):
    serializer_class = HotelProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # allows multipart/form-data requests (file uploads like images + normal form fields)

    def get_object(self):
        user = self.request.user

        if user.role != "hotel":
            raise ValidationError("Only guide users can access guide profile.")

        return user.hotel_profile

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
        try:
            hotel_profile = self.request.user.hotel_profile
        except HotelProfile.DoesNotExist:
            raise ValidationError("You must create a hotel profile before creating a room.")
        serializer.save(hotel=hotel_profile)
        from notifications.services import create_notification
        create_notification(
            recipient=self.request.user,
            notification_type="system",
            title="Room Created",
            message=f"Your room '{serializer.validated_data['room_type']}' has been successfully created.",
            related_object_id=serializer.instance.id  # Link to the created room
        )

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of rooms

class PackageCreateView(generics.CreateAPIView):
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a package

    def perform_create(self, serializer):
        if self.request.user.role != 'guide': # Check if the authenticated user has the role of 'guide'
            raise ValidationError("Only guide users can create packages.")
        try:
            guide_profile = self.request.user.guide_profile
        except GuideProfile.DoesNotExist:
            raise ValidationError("You must create a guide profile before creating a package.")
        serializer.save(guide=guide_profile)
        from notifications.services import create_notification
        create_notification(
            recipient=self.request.user,
            notification_type="system",
            title="Package Created",
            message=f"Your package '{serializer.validated_data['title']}' has been successfully created.",
            related_object_id=serializer.instance.id  # Link to the created package
        )

class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of packages