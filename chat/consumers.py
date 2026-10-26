import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .services import recent_messages, save_message

MAX_MESSAGE_LENGTH = 2000
TEACHERS_GROUP = "teachers"

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=text_data)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope["url_route"]["kwargs"]["room"]
        self.group = f"room_{self.room}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
        for message in await recent_messages(self.room):
            await self.send(text_data=json.dumps(message))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        if not isinstance(data, dict):
            return

        text = data.get("text")
        if not isinstance(text, str):
            return
        text = text.strip()
        if not text or len(text) > MAX_MESSAGE_LENGTH:
            return

        sender = data.get("sender", "anon")
        await save_message(self.room, sender, text)
        await self.channel_layer.group_send(
            self.group,
            {"type": "chat.message", "sender": sender, "text": text},
        )
        await self.channel_layer.group_send(
            TEACHERS_GROUP,
            {"type": "chat.message", "room": self.room, "sender": sender, "text": text},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"sender": event["sender"], "text": event["text"]}))


class TeacherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(TEACHERS_GROUP, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(TEACHERS_GROUP, self.channel_name)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"room": event["room"], "sender": event["sender"], "text": event["text"]}))