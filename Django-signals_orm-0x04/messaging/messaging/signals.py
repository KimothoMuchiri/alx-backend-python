from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Receiver function that listens for a new Message and creates 
    a Notification for the receiver.
    """
    # 1. Check if the message was actually created (not just updated)
    if created:
        # 2. Get the recipient of the message
        recipient = instance.receiver
        
        # 3. Define the notification content
        notification_content = f"New message from {instance.sender.username}: '{instance.content[:30]}...'"

        # 4. Create the Notification instance (the side-effect)
        Notification.objects.create(
            user=recipient,
            message=instance,
            content=notification_content
        )
        print(f"Successfully created notification for {recipient.username}")