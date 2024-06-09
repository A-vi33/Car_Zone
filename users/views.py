from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, OrderForm
from cars.models import Car
from .models import Order
def registerUser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('register')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
        
    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)

def loginUser(request):
    if request.method ==  'POST':
        form = AuthenticationForm(request, data= request.POST)
        username = request.POST['username'] 
        password = request.POST['password'] 
        if form.is_valid():
            user = authenticate(username=username, password=password)            
            if user is not None:
                login(request, user)
                messages.success(request, f"'{username}' logged in successfully")
                return redirect('home')
            else:
                messages.error(request, f"'{username}' user not found !!!") 
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, "Your Password is incorrect !!!")
            except:
                messages.error(request, f"'{username}' user not found !!!")
    else:
        form = AuthenticationForm()     
    return render(request, 'users/register.html', {'form': form})

def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout successfull !!!')
    return redirect('login')


def userProfile(request):
    user = request.user   
    context = {
        'user' :  user,
    }
    return render(request, 'users/profile.html', context )

def buyCar(request, car_id):
    car = Car.objects.get(pk=car_id)
    if(car.quantity > 0):
        car.quantity -= 1
        car.save()
        order = Order.objects.create(buyer=request.user, car=car)
    
    return redirect('car_details' , id=car_id)
    