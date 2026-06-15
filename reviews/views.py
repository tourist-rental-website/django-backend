from django.shortcuts import render
from .models import GuideReview, HotelReview
from .serializers import GuideReviewSerializer, HotelReviewSerializer
# fixed import casing and remove unused AllowAny
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class GuideReviewCreateView(generics.CreateAPIView):
    serializer_class = GuideReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

class GuideReviewListView(generics.ListAPIView):
    serializer_class = GuideReviewSerializer
    permission_classes = [AllowAny]
    queryset = GuideReview.objects.all()

class HotelReviewCreateView(generics.CreateAPIView):
    serializer_class = HotelReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)

class HotelReviewListView(generics.ListAPIView):
    serializer_class = HotelReviewSerializer
    permission_classes = [AllowAny]
    queryset = HotelReview.objects.all()