from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from listings.models import HotelProfile

User = get_user_model()


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    hotel = models.ForeignKey(HotelProfile, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'hotel']
    
    def __str__(self):
        return f"Conversation between guest {self.user.email} and hotel {self.hotel.hotel_name}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Message from {self.sender.email}"


class TypingIndicator(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='typing_indicators')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['conversation', 'user']
    
    def __str__(self):
        return f"{self.user.email} is typing"
