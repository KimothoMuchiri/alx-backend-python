from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','username','email']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only = True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    participants = UserSerializer(many = True, read_only = True)

    class Meta:
        model = Conversation
        fields = ['conversation_id','participants','created_at','messages']

    def get_messages(self, obj):
        messages_for_this_conversation = obj.message_set.all()
        serializer = MessageSerializer(messages_for_this_conversation, many=True)
        return serializer.data