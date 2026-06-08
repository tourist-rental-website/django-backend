from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title