from .models import GuideProfile, HotelProfile, Room, Package, RoomImage
from rest_framework import serializers

class GuideProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    phone = serializers.CharField(source='user.phone', required=False)
    profile_image = serializers.ImageField(source='user.profile_image', required=False)
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
        read_only_fields = ["created_at"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        # update user fields safely
        user = instance.user

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.phone = user_data.get("phone", user.phone)
        user.profile_image = user_data.get("profile_image", user.profile_image)

        user.save()

        # update guide profile fields
        instance.bio = validated_data.get("bio", instance.bio)
        instance.experience_years = validated_data.get("experience_years", instance.experience_years)
        instance.location = validated_data.get("location", instance.location)
        instance.price_per_day = validated_data.get("price_per_day", instance.price_per_day)

        instance.save()

        return instance

class HotelProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    phone = serializers.CharField(source='user.phone', required=False)
    profile_image = serializers.ImageField(source='user.profile_image', required=False)

    class Meta:
        model = HotelProfile
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
            "location",
            "created_at",
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.phone = user_data.get('phone', user.phone)
        user.profile_image = user_data.get('profile_image', user.profile_image)
        user.save()

        return super().update(instance, validated_data)
    
class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        read_only_fields = ['room']
        fields = ["id", "image", "uploaded_at"]

class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['hotel']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['guide']