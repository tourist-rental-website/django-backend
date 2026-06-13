from django.contrib import admin
from .models import Conversation, Message, TypingIndicator


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hotel', 'created_at', 'updated_at']
    search_fields = ['user__email', 'hotel__hotel_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation', 'created_at', 'is_read']
    search_fields = ['sender__email', 'content']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['created_at', 'read_at']


@admin.register(TypingIndicator)
class TypingIndicatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'conversation', 'created_at']
    search_fields = ['user__email']
