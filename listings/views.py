from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import GuideProfile, HotelProfile, Room, Package
from .serializers import GuideProfileSerializer, HotelProfileSerializer, RoomSerializer, PackageSerializer


class GuideProfileCreateView(generics.CreateAPIView):
    serializer_class = GuideProfileSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a guide profile

    def perform_create(self, serializer): 
        if self.request.user.role != 'guide': # Check if the authenticated user has the role of 'guide'
            raise ValidationError("Only guide users can create a guide profile.")
        serializer.save(user=self.request.user)
        #local import to avoid circular import issues since notifications also imports accounts and accounts imports notifications
        from notifications.services import create_notification

        create_notification(
            recipient=self.request.user,
            notification_type="system",
            title="Guide Profile Created",
            message="Your guide profile has been successfully created.",
            related_object_id=serializer.instance.id  # Link to the created guide profile
        )

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
        from notifications.services import create_notification
        create_notification(
            recipient=self.request.user,
            notification_type="system",
            title="Hotel Profile Created",
            message="Your hotel profile has been successfully created.",
            related_object_id=serializer.instance.id  # Link to the created hotel profile
        )

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