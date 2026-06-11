from django.shortcuts import render
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