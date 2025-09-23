from rest_framework import serializers
from .models import User, Message, Conversation
from .serializers import MessageSerializer, UserSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','username','email']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)

    class Meta:
        model = Message
        fields = ['message_id', 'sende_id', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessagerSerializer(many = True, read_only = True)
    participants = UserSerializer(many = True, read_only = True)

    class Meta:
        model = Conversation
        fields = ['conversation_id','participants_id','created_at','messages']