from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import GuideProfile
from .serializers import GuideProfileSerializer


class GuideProfileCreateView(generics.CreateAPIView):
    queryset = GuideProfile.objects.all()
    serializer_class = GuideProfileSerializer
    permission_classes = [IsAuthenticated]
