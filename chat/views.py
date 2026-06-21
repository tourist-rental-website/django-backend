from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Conversation, Message
from listings.models import HotelProfile
from .serializers import (
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer
)


class ConversationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        hotel_id = request.data.get('hotel_id')
        if not hotel_id:
            return Response(
                {'error': 'hotel_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            hotel = HotelProfile.objects.get(id=hotel_id)
        except HotelProfile.DoesNotExist:
            return Response(
                {'error': 'Hotel not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if hotel.user == request.user:
            return Response(
                {'error': 'You cannot start a conversation with your own hotel'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation, created = Conversation.objects.get_or_create(
            user=request.user,
            hotel=hotel
        )
        
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConversationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationListSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            hotel_profile = user.hotel_profile
            return Conversation.objects.filter(hotel=hotel_profile).prefetch_related('messages')
        except (AttributeError, HotelProfile.DoesNotExist):
            return Conversation.objects.filter(user=user).prefetch_related('messages')

    def post(self, request, *args, **kwargs):
        hotel_id = request.data.get('hotel_id')
        if not hotel_id:
            return Response(
                {'error': 'hotel_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            hotel = HotelProfile.objects.get(id=hotel_id)
        except HotelProfile.DoesNotExist:
            return Response(
                {'error': 'Hotel not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if hotel.user == request.user:
            return Response(
                {'error': 'You cannot start a conversation with your own hotel'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation, created = Conversation.objects.get_or_create(
            user=request.user,
            hotel=hotel
        )
        
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ConversationDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        try:
            hotel_profile = user.hotel_profile
            return Conversation.objects.filter(hotel=hotel_profile).prefetch_related('messages')
        except (AttributeError, HotelProfile.DoesNotExist):
            return Conversation.objects.filter(user=user).prefetch_related('messages')


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if conversation.user != request.user and conversation.hotel.user != request.user:
            return Response(
                {'error': 'You are not part of this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if conversation.user != request.user and conversation.hotel.user != request.user:
            return Response(
                {'error': 'You are not part of this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message_id = request.data.get('message_id')
        if not message_id:
            return Response(
                {'error': 'message_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            message = Message.objects.get(id=message_id, conversation=conversation)
            
            if message.sender == request.user:
                return Response(
                    {'error': 'You cannot mark your own message as read'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            message.is_read = True
            message.read_at = timezone.now()
            message.save()
            
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Message.objects.none()

        user = self.request.user
        if conversation.user != user and conversation.hotel.user != user:
            return Message.objects.none()

        return conversation.messages.all().order_by('created_at')
