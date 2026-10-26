import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .services import recent_messages, save_message


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
        data = json.loads(text_data)
        sender = data.get("sender", "anon")
        await save_message(self.room, sender, data["text"])
        await self.channel_layer.group_send(
            self.group,
            {"type": "chat.message", "sender": sender, "text": data["text"]},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"sender": event["sender"], "text": event["text"]}))