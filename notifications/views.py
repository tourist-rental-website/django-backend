from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    # Lists all notifications for the currently authenticated user
    # Only returns notifications belonging to request.user (not all notifications in the system)
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class UnreadNotificationListView(generics.ListAPIView):
    # Lists only unread notifications for the currently authenticated user
    # Useful for badge counts and unread notification panels
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        )


class MarkNotificationReadView(generics.UpdateAPIView):
    # Marks a single notification as read
    # Uses UpdateAPIView for standard update logic with minimal custom code
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow access to notifications belonging to the authenticated user
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        # Forces the notification to be marked as read regardless of request data
        serializer.save(is_read=True)


class MarkAllNotificationsReadView(APIView):
    # Marks ALL unread notifications as read for the authenticated user
    # Bulk operation — returns the count of updated notifications
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        updated_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        return Response({
            "message": f"{updated_count} notifications marked as read."
        })


class NotificationDeleteView(generics.DestroyAPIView):
    # Deletes a single notification — only if it belongs to the authenticated user
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class UnreadNotificationCountView(APIView):
    # Returns the count of unread notifications for the authenticated user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        return Response({
            "unread_count": unread_count
        })