from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


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

@receiver(pre_save, sender=Message)
def log_message_edit_history(sender, instance, **kwargs):
    """
    Captures the old content of a message and logs it to MessageHistory 
    BEFORE the new content is saved to the database.
    """
    # Check 1: Is this an existing message being updated?
    if instance.pk: 
        try:
            # Retrieve the current, non-updated version from the database
            original_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            # Should not happen, but safe to ignore if the object isn't found
            return

        # Check 2: Has the content actually changed?
        if original_message.content != instance.content:
            
            # 1. Log the original content to history (The decoupled side-effect)
            MessageHistory.objects.create(
                message=instance,
                old_content=original_message.content
            )
            print(f"Logged history for Message ID {instance.pk}. Old content: {original_message.content[:20]}...")

            # 2. Update the `edited` flag on the message instance
            # This change will be saved in the database during the current save() operation.
            instance.edited = True