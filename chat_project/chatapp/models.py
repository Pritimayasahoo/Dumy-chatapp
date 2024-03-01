from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .manager import CustomUserManager
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    createtime = models.DateTimeField(default=timezone.now)
    profileimg = models.ImageField(
        upload_to='profilepic', default='default.jpg')
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200, blank=True)
    mail = models.EmailField(unique=True)
    online_status = models.BooleanField(
        default=False)  # Field for online status
    last_seen = models.DateTimeField(
        null=True, blank=True)  # Field for last seen time

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    createtime = models.DateField(default=timezone.now)
    users = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name


class Chat(models.Model):
    context = models.CharField(max_length=1000)
    sendtime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.name
