from django.shortcuts import render
from .models import Car


def carDetails(request, id):
    car = Car.objects.get(pk=id)

    context = {
        'car' : car
    }
    return render(request, 'cars/car.html', context)
