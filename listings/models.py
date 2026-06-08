from django.db import models
from accounts.models import User


class GuideProfile(models.Model):
    user = models.OneToOneField(
        User,
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
    

    