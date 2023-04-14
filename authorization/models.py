from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    webhook_url = models.CharField(blank=True, max_length=255)
    receive_emails = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}, {self.username}'
    