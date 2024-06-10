from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from cars.models import Car
from .models import Order


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
        
    context = {
        'form' : form,
        'type' : 'Register'
    }
    return render(request, 'users/register.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
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
    return render(request, 'users/register.html', {'form': form, 'type' : 'Login'})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout successfull !!!')
    return redirect('login')


@login_required(login_url='login')
def userProfile(request):
    user = request.user   
    context = {
        'user' :  user,
    }
    return render(request, 'users/profile.html', context )

@login_required(login_url='login')
def buyCar(request, car_id):
    car = Car.objects.get(pk=car_id)
    if(car.quantity > 0):
        car.quantity -= 1
        car.save()
        order = Order.objects.create(buyer=request.user, car=car)
    else:
        messages.warning(request, 'Sorry this car is stock out !!!')
    
    return redirect('car_details' , id=car_id)
    

def updateProfile(request):
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account of "{username}" updated successfully  !!!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
        
    context = {
        'form' : form,
        'type' : 'Update Profile'
    }
    return render(request, 'users/register.html', context)

def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user= request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfull !!!')
            return redirect('profile')
    else:
        form=PasswordChangeForm(user= request.user)    
    return render(request, 'users/register.html', {'form':form, 'type':'Change Password'})
    