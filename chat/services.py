from channels.db import database_sync_to_async

from .models import Message


@database_sync_to_async
def save_message(room, sender, text):
    return Message.objects.create(room=room, sender=sender, text=text)


@database_sync_to_async
def recent_messages(room, limit=50):
    messages = list(Message.objects.filter(room=room).order_by("-created_at")[:limit])
    return [{"sender": m.sender, "text": m.text} for m in reversed(messages)]