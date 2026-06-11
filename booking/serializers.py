from .models import RoomBooking, PackageBooking
from rest_framework import serializers

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = "__all__"
        read_only_fields = ["traveler", "status", "created_at"]

class PackageBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageBooking
        fields = "__all__"
        read_only_fields = ["traveler", "status", "created_at"]