import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):  
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'chat_{self.room_id}'

        if not await self.check_room_access():
            await self.close()

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

    # Получаем сообщение от WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        # Получаем пользователя и сохраняем сообщение в БД
        user = self.scope["user"]
        if not isinstance(user, AnonymousUser):
            print('validation')
            await self.save_message(user, self.room_id, message)

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username
            }
        )

    # Получаем сообщение из группы
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Отправляем сообщение обратно WebSocket-клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, user, room_id, message):
        from .models import Message
        Message.objects.create(
            room_id=room_id,  # Используем room_id вместо полного объекта
            sender=user,
            content=message,
            timestamp=sync_to_async(datetime.now)
        )

    @database_sync_to_async
    def check_room_access(self):
        return self.scope["user"].rooms.filter(id=self.room_id).exists()
    