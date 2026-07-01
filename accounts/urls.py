from django.urls import path
from .views import (
    RegisterView, MeView, 
    VerifyEmailView, CustomTokenObtainPairView, 
    GoogleOAuthView, ForgetPasswordView, ResetPasswordView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view()), # This view will handle user login and return JWT(acess and refresh) tokens
    path("google/", GoogleOAuthView.as_view(), name="google-oauth"), # This view will handle Google OAuth login and return JWT tokens
    path("api/token/refresh/", TokenRefreshView.as_view()), # This view will handle refreshing JWT access tokens
    path("me/", MeView.as_view(), name="me"), # This view will return the details of the currently authenticated user
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("forget-password/", ForgetPasswordView.as_view(), name="forget-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),

]

