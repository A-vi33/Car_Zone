from django.db import models
from brands.models import Brand


class Car(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='cars/upload/', blank=True, null=True)
    mileage = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    

    
    
