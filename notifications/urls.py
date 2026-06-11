from django.urls import path
from .views import (
    NotificationDeleteView,
    NotificationListView,
    UnreadNotificationCountView,
    UnreadNotificationListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("unread/", UnreadNotificationListView.as_view(), name="notification-unread"),
    path("<int:pk>/read/", MarkNotificationReadView.as_view(), name="notification-read"),
    path("read-all/", MarkAllNotificationsReadView.as_view(), name="notification-read-all"),
    path("<int:pk>/delete/", NotificationDeleteView.as_view(), name="notification-delete"),
    path("count/unread/", UnreadNotificationCountView.as_view(), name="notification-unread-count"),
]
