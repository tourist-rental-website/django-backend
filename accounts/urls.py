from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view()), # This view will handle user login and return JWT(acess and refresh) tokens
    path("api/token/refresh/", TokenRefreshView.as_view()), # This view will handle refreshing JWT access tokens
]

