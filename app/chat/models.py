import uuid

from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='rooms')
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'from user {self.sender} at {self.timestamp}'
