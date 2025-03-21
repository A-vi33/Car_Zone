from django.db import models

from django.contrib.auth.models import User
from django.db.models import CharField

from cars.models import Car

# In users/models.py
from django.db import models
from django.contrib.auth.models import User
from cars.models import Car

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    address = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100,default=CharField)
    state = models.CharField(max_length=100)
    postal_code = models.IntegerField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s address"