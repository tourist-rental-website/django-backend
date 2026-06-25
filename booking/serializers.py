from .models import RoomBooking, PackageBooking
from rest_framework import serializers

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = "__all__"
        read_only_fields = ["traveler", "status", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        from listings.serializers import RoomSerializer
        representation['room'] = RoomSerializer(instance.room).data
        return representation

class PackageBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageBooking
        fields = "__all__"
        read_only_fields = ["traveler", "status", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        from listings.serializers import PackageSerializer
        representation['package'] = PackageSerializer(instance.package).data
        return representation