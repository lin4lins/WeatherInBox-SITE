from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    webhook_url = models.CharField(blank=True, max_length=255)
    receive_emails = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id}, {self.username}'
    