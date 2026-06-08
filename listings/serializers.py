from .models import GuideProfile
from rest_framework import serializers

class GuideProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideProfile
        fields = '__all__'