from django.shortcuts import render, redirect
from .models import Car
from .forms import CommentForm
from django.contrib import messages

def carDetails(request, id):
    car = Car.objects.get(pk=id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.save()    
            messages.success(request, 'Commented successfull !!!')
            return redirect('car_details', id =id)
    else:
        form = CommentForm()
        
    
    context = {
        'car' : car,
        'comment_form': form
    }
    return render(request, 'cars/car.html', context)
