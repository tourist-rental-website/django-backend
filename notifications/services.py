from .models import Notification


def create_notification(recipient, notification_type, title, message):
    """
    Reusable helper to create a notification for a user.

    Usage from any app:
        from notifications.services import create_notification
        create_notification(
            recipient=some_user,
            notification_type="booking",
            title="Booking Confirmed",
            message="Your booking for Deluxe Room has been confirmed."
        )
    """
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
    )
