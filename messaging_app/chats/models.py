import uuid
from django.db import models(
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length = 30, null = False)
    last_name = models.CharField(max_length = 30, null = False)
    email = models.EmailField(unique = True)
    # password_hash = models.CharField(min_length = 8 , null = False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length = 5, choices= ROLE_CHOICES, default = 'guest', null = False)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    participants_id = models.ManyToManyField('chats.User')
    created_at = models.DateTimeField(auto_now_add= True)
    

class Message(models.Model):
    message_id = models.UUIDField(default = uuid.uuid4, primary_key= True, editable= False)
    sender_id = models.ForeignKey('chats.User', on_delete=models.CASCADE)
    conversation = models.ForeignKey('chats.Conversation', on_delete = models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add = True)
# Create your models here.
