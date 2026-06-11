from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from jsonschema import ValidationError
from .models import RoomBooking, PackageBooking
from .serializers import RoomBookingSerializer, PackageBookingSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RoomBookingCreateView(generics.CreateAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'traveler': # Check if the authenticated user has the role of 'traveler'
            raise ValidationError("Only traveler users can create room bookings.")
        serializer.save(traveler=self.request.user)

class PackageBookingCreateView(generics.CreateAPIView):
    serializer_class = PackageBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

class MyBookingsView(generics.ListAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoomBooking.objects.filter(traveler=self.request.user)
    
class MyPackageBookingsView(generics.ListAPIView):
    serializer_class = PackageBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PackageBooking.objects.filter(traveler=self.request.user)


class CancelRoomBookingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        booking = get_object_or_404(
            RoomBooking,
            id=self.kwargs["pk"],
            traveler=request.user
        )

        booking.status = "cancelled"
        booking.save()

        return Response({
            "message": "Booking cancelled successfully."
        })
    
class CancelPackageBookingView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        booking = get_object_or_404(
            PackageBooking,
            id=self.kwargs["pk"],
            traveler=request.user
        )

        booking.status = "cancelled"
        booking.save()

        return Response({
            "message": "Booking cancelled successfully."
        })