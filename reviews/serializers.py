from .models import GuideReview, HotelReview
from rest_framework import serializers  

class GuideReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideReview
        fields = ['id', 'traveler', 'guide', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

class HotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = ['id', 'traveler', 'hotel', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']