from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Subscription(models.Model):
    city_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    times_per_day = models.IntegerField(default=1, validators=[MaxValueValidator(12), MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
