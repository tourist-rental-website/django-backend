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
        return Notification.objects.filter(recipient=self.request.user, is_read=False)


class MarkNotificationReadView(APIView):
    # Marks a single notification as read
    # Uses APIView (same as MeView in accounts) for custom logic beyond simple CRUD
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=404)

        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class MarkAllNotificationsReadView(APIView):
    # Marks ALL unread notifications as read for the authenticated user
    # Bulk operation — returns the count of updated notifications
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        updated_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        return Response({"message": f"{updated_count} notifications marked as read."})
