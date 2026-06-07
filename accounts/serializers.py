from rest_framework import serializers
from .models import User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
        ]
        read_only_fields = ["id", "email", "role"] # id and email cannot be updated by the user