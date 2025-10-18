from django.contrib.auth.models import User
from app_name.models import Message, Notification

# 1. Create two users
user_a = User.objects.create_user(username='alice', password='password')
user_b = User.objects.create_user(username='bob', password='password')

# 2. Create a new message from Alice to Bob
# This single .create() call TRIGGERS the signal!
message = Message.objects.create(
    sender=user_a, 
    receiver=user_b, 
    content="Hey Bob, dinner tonight?"
)

# 3. Check the notifications for Bob
# You should see one notification record
bob_notifications = Notification.objects.filter(user=user_b)
print(bob_notifications)
# Expected Output: <QuerySet [<Notification: Notification for bob: New message from alice: 'Hey Bob, dinner to...'>]>

# 4. Verify the signal DID NOT fire for Alice
alice_notifications = Notification.objects.filter(user=user_a)
print(alice_notifications)
# Expected Output: <QuerySet []>

### Test two
# 1. Import necessary models
from django.contrib.auth.models import User
from messaging.models import Message, MessageHistory

# 2. Create the users Alice and Bob
user_a = User.objects.create_user(username='alice', password='password123', email='alice@example.com')
user_b = User.objects.create_user(username='bob', password='password123', email='bob@example.com')

print(f"Users created: Alice (ID: {user_a.id}) and Bob (ID: {user_b.id})")
print("-------------------------------------------------------")

# 3. Create a message (pre_save fires, but no history is logged because it's new)
m = Message.objects.create(
    sender=user_a, 
    receiver=user_b, 
    content="Initial message content. This will be logged on the first edit."
)
print(f"Message ID: {m.id}, Content: '{m.content[:20]}...', Edited: {m.edited}")
# Expected Output: Edited: False (No history yet)

# 4. Check history BEFORE edit
print(f"History records BEFORE edit: {m.history.count()}") 
# Expected Output: History records BEFORE edit: 0

# 5. Edit the message content (This triggers the pre_save signal, logging history)
m.content = "Revised content: The original content has been updated."
m.save() # <-- pre_save runs here, logs the old content, sets m.edited=True

print(f"\nMessage ID: {m.id} AFTER SAVE:")
print(f"New Content: '{m.content[:20]}...'")
print(f"Edited Flag: {m.edited}")
# Expected Output: Edited Flag: True

# 6. Check the history records AFTER edit
history_records = m.history.all().order_by('edited_at')

print("\n--- Message History Log ---")
print(f"Total history records: {history_records.count()}")
# Expected Output: Total history records: 1

for record in history_records:
    print(f"Logged Content (Old): '{record.old_content}'")
# Expected Output: Logged Content (Old): 'Initial message content. This will be logged on the first edit.'