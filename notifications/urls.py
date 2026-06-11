from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("unread/", UnreadNotificationListView.as_view(), name="notification-unread"),
    path("<int:pk>/read/", MarkNotificationReadView.as_view(), name="notification-read"),
    path("read-all/", MarkAllNotificationsReadView.as_view(), name="notification-read-all"),
]
