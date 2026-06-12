from django.db import models
from accounts.models import User


class Notification(models.Model):
    # ForeignKey to User — each notification belongs to a single user (the recipient)
    # related_name allows reverse lookup: user.notifications.all()
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    related_object_id = models.PositiveIntegerField(
        blank=True, 
        null=True
    )

    # Notification type to allow client-side filtering and icon/styling decisions
    TYPE_CHOICES = (
        ("booking_created", "Booking Created"),
        ("booking_approved", "Booking Approved"),
        ("booking_rejected", "Booking Rejected"),
        ("new_message", "New Message"),
        ("review_received", "Review Received"),
        ("payment_success", "Payment Success"),
        ("system", "System"),
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="system")

    title = models.CharField(max_length=255)  # Short headline shown in notification list
    message = models.TextField()               # Full notification body/detail text

    is_read = models.BooleanField(default=False)  # Track whether the user has seen this notification

    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set when notification is created

    class Meta:
        ordering = ['-created_at']  # Most recent notifications first

    def __str__(self):
        return f"{self.notification_type}: {self.title} → {self.recipient.email}"
