from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Subscription(models.Model):
    FREQUENCIES = [
        (1, "1"),
        (2, "2"),
        (4, "4"),
        (6, "6"),
        (12, "12"),
    ]
    city_id = models.IntegerField()
    times_per_day = models.IntegerField(default=1, choices=FREQUENCIES)
    is_active = models.BooleanField(default=True)
