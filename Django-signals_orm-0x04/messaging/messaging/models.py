from django.db import models
from django.contrib.auth import get_user_model

# Use the standard Django User model
User = get_user_model() 

class Message(models.Model):
    """Represents a direct message between users."""
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    #field to track if the message has ever been edited
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

class MessageHistory(models.Model):
    """Stores the old versions of a Message every time it is edited."""
    
    # Link to the current Message object
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    
    # The content *before* the current save operation
    old_content = models.TextField() 
    
    # When this historical record was created (when the edit happened)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} recorded at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"

class Notification(models.Model):
    """Stores a record of a notification for a user."""
    # The user who needs to see the notification
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE) 
    
    # The specific message that triggered this notification
    message = models.ForeignKey(Message, related_name='related_notification', on_delete=models.CASCADE) 
    
    content = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content}"