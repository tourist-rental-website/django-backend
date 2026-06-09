from django.db import models
from accounts.models import User


class GuideProfile(models.Model):
    user = models.OneToOneField( # One-to-one relationship with User model, just like foregin key but only one guide profile per user 
        User,                    # whereas foreign key allows multiple guide profiles for a single user
        on_delete=models.CASCADE,
        related_name="guide_profile"
    )

    bio = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    languages = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guide: {self.user.email}"
    

class HotelProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="hotel_profile"
    )

    hotel_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hotel_name