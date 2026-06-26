from django.urls import path
from .views import RegisterView, MeView, VerifyEmailView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view()), # This view will handle user login and return JWT(acess and refresh) tokens
    path("api/token/refresh/", TokenRefreshView.as_view()), # This view will handle refreshing JWT access tokens
    path("me/", MeView.as_view(), name="me"), # This view will return the details of the currently authenticated user
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
]

