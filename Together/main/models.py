""" Main App models """
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
         return self.name


class Room(models.Model):
    """ Room Model that represents the rooms table """
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    """ Message Model that represents the messages table """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
            return self.body[0:50]
    