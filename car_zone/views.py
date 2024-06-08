from django.shortcuts import render
from cars.models import Car
from brands.models import Brand

def home(request, brand_slug=None):
    cars = Car.objects.all()
    brands = Brand.objects.all()
    
    if brand_slug is not None:
        brand = Brand.objects.get(slug=brand_slug)
        cars = Car.objects.filter(brand=brand)
    
    context= {
        'cars':cars,
        'brands':brands,
    }
    print(cars)
    return render(request, 'home.html', context)