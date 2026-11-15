from channels.db import database_sync_to_async

from .models import Message


@database_sync_to_async
def save_message(room, sender, text):
    return Message.objects.create(room=room, sender=sender, text=text)


@database_sync_to_async
def recent_messages(room, limit=50):
    messages = list(Message.objects.filter(room=room).order_by("-created_at")[:limit])
    return [{"sender": m.sender, "text": m.text, "time": m.created_at.isoformat()} for m in reversed(messages)]


@database_sync_to_async
def recent_messages_all_rooms(limit=100):
    messages = list(Message.objects.order_by("-created_at")[:limit])
    return [{"room": m.room, "sender": m.sender, "text": m.text, "time": m.created_at.isoformat()} for m in reversed(messages)]