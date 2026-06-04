from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Template URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # API URLs for authentication and user details
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
]