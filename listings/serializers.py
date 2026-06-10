from .models import GuideProfile, HotelProfile, Package, Room
from rest_framework import serializers

class GuideProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideProfile
        fields = '__all__'
        read_only_fields = ['user'] # This ensures that the user field is not included in the input data when creating or updating a guide profile, and it will be set automatically based on the authenticated user making the request
        

class HotelProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelProfile
        fields = '__all__'
        read_only_fields = ['user']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'
        read_only_fields=['hotel'] # Hotel is set automatically via perform_create(), not sent by client


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['guide'] # Guide is set automatically via perform_create(), not sent by client