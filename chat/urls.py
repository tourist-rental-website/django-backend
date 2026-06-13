from django.urls import path
from .views import (
    ConversationCreateView,
    ConversationListView,
    ConversationDetailView,
    SendMessageView,
    MarkAsReadView,
    MessageListView,
)

urlpatterns = [
    path("conversations/create/", ConversationCreateView.as_view(), name="conversation-create"),
    path("conversations/", ConversationListView.as_view(), name="conversation-list"),
    path("conversations/<int:pk>/", ConversationDetailView.as_view(), name="conversation-detail"),
    path("conversations/<int:pk>/send_message/", SendMessageView.as_view(), name="conversation-send-message"),
    path("conversations/<int:pk>/mark_as_read/", MarkAsReadView.as_view(), name="conversation-mark-as-read"),
    path("conversations/<int:pk>/messages/", MessageListView.as_view(), name="conversation-messages"),
]
