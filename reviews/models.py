from django.db import models
from accounts.models import User
from listings.models import GuideProfile, HotelProfile
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class GuideReview(models.Model):
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guide_reviews')
    guide = models.ForeignKey(GuideProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ]
    )
    comment = models.TextField(blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)

class HotelReview(models.Model):
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_reviews')
    hotel = models.ForeignKey(HotelProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ]
    )
    comment = models.TextField(blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)