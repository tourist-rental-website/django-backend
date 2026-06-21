from .models import GuideProfile, HotelProfile, Room, Package
from rest_framework import serializers

class GuideProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone = serializers.CharField(source='user.phone')
    profile_image = serializers.ImageField(source='user.profile_image')
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = GuideProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_image",
            "bio",
            "experience_years",
            "location",
            "price_per_day",
            "created_at",
            "role"
        ]
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        user.role = instance.role
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.phone = user_data.get('phone', user.phone)
        user.profile_image = user_data.get('profile_image', user.profile_image)
        user.save()

        return super().update(instance, validated_data)
        

class HotelProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone = serializers.CharField(source='user.phone')
    profile_image = serializers.ImageField(source='user.profile_image')

    class Meta:
        model = GuideProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_image",
            "hotel_name",
            "description",
            "contact_number",
            "location"
        ]
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.phone = user_data.get('phone', user.phone)
        user.profile_image = user_data.get('profile_image', user.profile_image)
        user.save()

        return super().update(instance, validated_data)
    class Meta:
        model = HotelProfile
        fields = '__all__'
        read_only_fields = ['user']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['hotel']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['guide']