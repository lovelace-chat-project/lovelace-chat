from django.db import models


class Message(models.Model):
    room = models.CharField(max_length=200)
    sender = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["room", "created_at"])]