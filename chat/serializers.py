from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message, TypingIndicator
from listings.serializers import HotelProfileSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'created_at', 'is_read', 'read_at']
        read_only_fields = ['created_at', 'read_at']

class ConversationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hotel = HotelProfileSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'hotel', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ConversationListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hotel = HotelProfileSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'hotel', 'last_message', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None


class TypingIndicatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TypingIndicator
        fields = ['id', 'user', 'created_at']
