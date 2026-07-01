from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from listings.models import GuideProfile, HotelProfile
from .models import TravelerProfile

def create_user_profile(user):
    """
    Creates the corresponding profile based on the user's role.
    """

    if user.role == "traveler":
        profile, _ = TravelerProfile.objects.get_or_create(user=user)

    elif user.role == "guide":
        profile, _ = GuideProfile.objects.get_or_create(user=user)

    elif user.role == "hotel":
        profile, _ = HotelProfile.objects.get_or_create(user=user)

    else:
        profile = None

    return profile


def getprofile(user):
    """
    Returns the user's profile by role, creating it if needed.
    """
    return create_user_profile(user)


def send_verification_email(user):
    """
    Generates a verification link and sends it to the user's email.
    """
    
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verification_url = (
        f"{settings.DJANGO_URL}/verify-email/{uid}/{token}/"
    )

    send_mail(
        subject="Verify your Email",
        message=(
            f"Hi {user.first_name},\n\n"
            f"Thank you for registering.\n\n"
            f"Please verify your email by clicking the link below:\n\n"
            f"{verification_url}\n\n"
            f"If you didn't create this account, you can safely ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )