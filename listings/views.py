from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import GuideProfile
from .serializers import GuideProfileSerializer


class GuideProfileCreateView(generics.CreateAPIView):
    serializer_class = GuideProfileSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create a guide profile

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

class GuideProfileListView(generics.ListAPIView):
    queryset = GuideProfile.objects.all()
    serializer_class = GuideProfileSerializer
    permission_classes = [AllowAny] # Unauthenticated users can also view the list of guides