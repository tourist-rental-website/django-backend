import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import Conversation, Message, TypingIndicator
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.conversation_id}'
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        conversation = await sync_to_async(self.get_conversation)()
        if not conversation or (conversation.user != self.user and conversation.hotel.user != self.user):
            await self.close()
            return
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name') and hasattr(self, 'channel_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if hasattr(self, 'conversation_id'):
            await sync_to_async(self.remove_typing_indicator)()
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'message':
                await self.handle_message(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'read_receipt':
                await self.handle_read_receipt(data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))
    
    async def handle_message(self, data):
        content = data.get('content')
        if not content:
            await self.send(text_data=json.dumps({'error': 'content is required'}))
            return
        
        message = await sync_to_async(self.create_message)(content)
        serializer_data = await sync_to_async(lambda: MessageSerializer(message).data)()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serializer_data
            }
        )
    
    async def handle_typing(self, data):
        is_typing = data.get('is_typing', False)
        
        if is_typing:
            await sync_to_async(self.create_or_update_typing_indicator)()
        else:
            await sync_to_async(self.remove_typing_indicator)()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': self.user.id,
                'user_email': self.user.email,
                'is_typing': is_typing
            }
        )
    
    async def handle_read_receipt(self, data):
        message_id = data.get('message_id')
        if not message_id:
            return
        
        await sync_to_async(self.mark_message_as_read)(message_id)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'read_receipt',
                'message_id': message_id,
                'user_id': self.user.id
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message']
        }))
    
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'user_email': event['user_email'],
            'is_typing': event['is_typing']
        }))
    
    async def read_receipt(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'message_id': event['message_id'],
            'user_id': event['user_id']
        }))
    
    def get_conversation(self):
        try:
            return Conversation.objects.select_related('hotel__user', 'user').get(id=self.conversation_id)
        except Conversation.DoesNotExist:
            return None
    
    def create_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content
        )
    
    def create_or_update_typing_indicator(self):
        conversation = Conversation.objects.get(id=self.conversation_id)
        TypingIndicator.objects.update_or_create(
            conversation=conversation,
            user=self.user
        )
    
    def remove_typing_indicator(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            TypingIndicator.objects.filter(conversation=conversation, user=self.user).delete()
        except Conversation.DoesNotExist:
            pass
    
    def mark_message_as_read(self, message_id):
        try:
            message = Message.objects.get(id=message_id, conversation_id=self.conversation_id)
            if message.sender == self.user:
                return
            message.is_read = True
            message.read_at = timezone.now()
            message.save()
        except Message.DoesNotExist:
            pass
