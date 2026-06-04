from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserDetailSerializer

User = get_user_model()

# Template views (for standard HTML forms)
def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    context = {
        'title': ("Register"),
        'page_title': ("Register Account"),
        'page_description': ('this is the registration page'),
    }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    return render(request, 'accounts/login.html')


# API views (for JSON/JWT authentication)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens upon registration
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user