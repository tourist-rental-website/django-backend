from rest_framework import serializers
from .models import User,TravelerProfile

class RegisterSerializer(serializers.ModelSerializer):
    # Inherits from ModelSerializer to automatically generate fields from the User model
    # This serializer handles validation and deserialization of registration data

    # Override the default password field because:
    # 1. write_only=True prevents password from appearing in API responses (security)
    # 2. min_length=8 adds validation that auto-generation cannot infer from the model
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        # Bind this serializer to the User model
        model = User

        # Whitelist only these fields — anything not listed is ignored
        # in both incoming requests and outgoing responses
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "role",
        )

    def create(self, validated_data):
        # Called when serializer.save() is invoked on a POST request
        # Uses create_user() instead of create() because:
        # 1. create_user() hashes the password before saving to the database
        # 2. Plain create() would store the password in plaintext (security risk)
        # **validated_data unpacks the cleaned fields as keyword arguments
        return User.objects.create_user(**validated_data)
    


#User Serializer hataideko yesbata ani traveler serializer banako

class TravelerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone = serializers.CharField(source='user.phone')
    profile_image = serializers.ImageField(source='user.profile_image')
    role = serializers.CharField(source='user.role', read_only=True)
    class Meta:
        model = TravelerProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "profile_image",
            "role"
        ]
        read_only_fields=['user']
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.phone = user_data.get('phone', user.phone)
        user.profile_image = user_data.get('profile_image', user.profile_image)
        user.save()

        return super().update(instance, validated_data)