from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Assuming request.data contains a list of participant user IDs
        participant_ids = request.data.get('participants', [])
        participants = User.objects.filter(id__in=participant_ids)

        # Create the conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(*participants)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Create your views here.
class MessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get('conversation')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=request.data.get('message_body')
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
