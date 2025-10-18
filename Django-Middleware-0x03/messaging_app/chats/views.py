from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOrReadOnly, IsParticipantOfConversation # <-- Import the OLP class
from django_filters.rest_framework import DjangoFilterBackend # <-- Need this import!
from .filters import MessageFilter 

class ConversationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('participants',)

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
    permission_classes = [IsParticipantOfConversation]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        user = self.request.user
        
        # 1. Start with all messages
        queryset = Message.objects.all()
        
        # 2. Filter to include only messages linked to conversations 
        #    where the current user is a participant.
        #    (Assuming Message has a ForeignKey to Conversation)
        return queryset.filter(
            conversation__participants=user.pk
        ).distinct()

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

    def perform_create(self, serializer):
        # The serializer save method accepts additional keyword arguments, 
        # which are passed to the Model.objects.create() method.
        # We pass the authenticated user from the request to the 'sender' field.
        serializer.save(sender=self.request.user) 
