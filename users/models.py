from django.db import models

from django.contrib.auth.models import User
from cars.models import Car

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    