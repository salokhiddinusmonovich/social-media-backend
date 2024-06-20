from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User)

    def str(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.room.name