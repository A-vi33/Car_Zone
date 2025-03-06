import razorpay
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from car_zone import settings
from .forms import UserRegisterForm, UserUpdateForm
from cars.models import Car
from .models import Order
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import AddressForm



class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def get(self, request,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the user first
        user = form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')  # Assuming password1 is your password field

        # Prepare email content
        subject = 'Welcome to Our Site - Your Login Credentials'
        message = f"""
        Hello {username},

        Your account has been successfully created! Here are your login credentials:

        Username: {username}
        Password: {password}

        Please login at {self.request.build_absolute_uri(reverse_lazy('login'))}
        and change your password after your first login.

        Regards,
        The Team
        """

        # Send email
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(self.request,
                             f'Account created successfully for {username}! Check your email for login credentials.')
        except Exception as e:
            # Handle email sending failure gracefully
            messages.warning(self.request,
                             f'Account created successfully for {username}, but failed to send email: {str(e)}')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context
    




class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/register.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)            
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"'{username}' logged in successfully")
            return redirect('home')
        else:
            messages.error(self.request, f"'{username}' user not found !!!") 
        return super().form_valid(form)

    def form_invalid(self, form):
        username = self.request.POST.get('username')
        try:
            User.objects.get(username=username)
            messages.error(self.request, "Your Password is incorrect !!!")
        except:
            messages.error(self.request, f"'{username}' user not found !!!")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
    
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
    try:
        car = Car.objects.get(pk=car_id)

        if car.quantity <= 0:
            messages.warning(request, 'Sorry, this car is out of stock!')
            return redirect('car_details', id=car_id)

        # Store car details in session
        request.session['car_details'] = {
            'id': car.id,
            'name': car.name,
            'price': str(car.price),  # Convert Decimal to string
            'brand': car.brand.name
        }
        # Debug: Confirm session data
        print("Car details stored in session:", request.session['car_details'])

        # Check for address details
        if not request.session.get('address_details'):
            messages.info(request, 'Please provide your delivery address.')
            return redirect('add_delivery_address')

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        order_amount = int(float(car.price) * 100)  # Convert to paise

        payment_data = {
            'amount': order_amount,
            'currency': 'INR',
            'receipt': f'order_rcptid_{car.id}',
            'notes': {
                'car_id': car.id,
                'user_id': request.user.id,
                'email': request.user.email
            }
        }

        # Create Razorpay order
        razorpay_order = client.order.create(data=payment_data)
        request.session['razorpay_order_id'] = razorpay_order['id']
        print("Razorpay order ID stored in session:", request.session['razorpay_order_id'])

        context = {
            'car': car,
            'order_id': razorpay_order['id'],
            'amount': order_amount,
            'key_id': settings.RAZORPAY_API_KEY,
            'user_name': f"{request.user.first_name} {request.user.last_name}",
            'user_email': request.user.email,
            'user_contact': request.user.profile.phone if hasattr(request.user, 'profile') else ''
        }

        return render(request, 'users/payment.html', context)

    except Car.DoesNotExist:
        messages.error(request, 'Car not found.')
        return redirect('home')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('home')


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
    
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/register.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['type'] = 'Change Password'
        return context







@login_required(login_url='login')
def initiatePayment(request):
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Define the amount (e.g., ₹1000 for testing purposes)
    dynamic_amount = 1000
    order_amount = int(dynamic_amount * 100)  # ₹1000 in paise
    order_currency = 'INR'
    order_receipt = f'order_rcptid_{request.user.id}'
    notes = {'user_id': request.user.id, 'purpose': 'Adding funds to account'}

    # Create a Razorpay order
    razorpay_order = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'notes': notes
    })

    # Save the Razorpay order ID in the session for verification later
    request.session['razorpay_order_id'] = razorpay_order['id']

    # Pass the Razorpay order details to the template
    context = {
        'order_id': razorpay_order['id'],
        'amount': order_amount,
        'key_id': 'rzp_test_Ty2fPZgb35aMIa',
    }
    return render(request, 'users/payment.html', context)

def paymentsuccess(request):
    sub='Car_Zone'
    msg='Thanks form Buying....!!'
    frm='mohith202421@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub,
        msg,
        frm,
        [to]    ,
        fail_silently=False
    )
    return render(request,'users/paymentsuccess.html')





def send_order_confirmation_email(user, car):
    subject = 'Order Confirmation - Car Zone'

    message = f"""

    Dear {user.first_name},


    Thank you for your purchase from Car Zone!


    Order Details:

    Car: {car.name}

    Brand: {car.brand}

    Price: ₹{car.price}


    Your car will be delivered within 4 days.


    Thank you for choosing Car Zone!


    Best regards,

    Car Zone Team

    """

    send_mail(

        subject,

        message,

        settings.EMAIL_HOST_USER,

        [user.email],

        fail_silently=False,

    )

@csrf_exempt
def paymentHandler(request):
    if request.method == 'POST':
        try:
            # Debug: Print session data
            print("Session ID:", request.session.session_key)
            print("Session data in paymentHandler:", dict(request.session.items()))

            # Get car details from session
            car_details = request.session.get('car_details')
            if not car_details:
                # Fallback: Recover from Razorpay order notes
                order_id = request.POST.get('razorpay_order_id')
                client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
                order_data = client.order.fetch(order_id)
                car_id = order_data['notes'].get('car_id')
                if car_id:
                    car = Car.objects.get(pk=car_id)
                    car_details = {
                        'id': car.id,
                        'name': car.name,
                        'price': str(car.price),
                        'brand': car.brand.name
                    }
                    print("Recovered car_details from order notes:", car_details)
                else:
                    messages.error(request, 'Car details not found in session or order. Please try again.')
                    return redirect('home')

            # Get payment details
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            if not all([payment_id, order_id, signature]):
                messages.error(request, 'Missing payment information.')
                return redirect('home')

            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)

            # Get car and create order
            car = Car.objects.get(pk=car_details['id'])
            order = Order.objects.create(
                user=request.user,               # Matches 'user' field
                car=car,                         # Matches 'car' field
                payment_id=payment_id,           # Matches 'payment_id' field
                address=request.session.get('address_details', {})  # Matches 'address' field
            )

            # Update car quantity
            car.quantity -= 1
            car.save()

            # Send confirmation email
            subject = 'Car Purchase Confirmation - Car Zone'
            html_message = render_to_string('users/order_confirmation.html', {
                'username': request.user.username,
                'car_name': car.name,
                'amount': car.price,
                'delivery_time': 4,
                'address': request.session.get('address_details', {})
            })
            send_mail(
                subject,
                strip_tags(html_message),
                settings.EMAIL_HOST_USER,
                [request.user.email],
                html_message=html_message,
                fail_silently=False
            )

            # Clear session data
            for key in ['car_details', 'address_details', 'razorpay_order_id']:
                request.session.pop(key, None)

            messages.success(request, 'Payment successful! Your order has been placed.')
            return redirect('payment_success')

        except Car.DoesNotExist:
            messages.error(request, 'Car not found in database. Please contact support.')
            return redirect('home')
        except razorpay.errors.SignatureVerificationError as e:
            messages.error(request, f'Payment verification failed: {str(e)}')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Payment processing failed: {str(e)}')
            return redirect('home')

    return HttpResponseBadRequest('Invalid request method')


@login_required(login_url='login')
def save_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            # Save address details to session
            request.session['address_details'] = address_form.cleaned_data
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': address_form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required(login_url='login')
def addDeliveryAddress(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            # Save address details to session
            request.session['address_details'] = address_form.cleaned_data
            print("Address details stored in session:", request.session['address_details'])

            # Check if car_details exists
            car_details = request.session.get('car_details')
            if not car_details:
                messages.error(request, 'Car details not found in session. Please try again.')
                return redirect('home')

            messages.success(request, 'Address saved successfully!')
            return redirect('buy_car', car_id=car_details['id'])
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        address_form = AddressForm()

    context = {
        'address_form': address_form,
    }
    return render(request, 'users/add_address.html', context)

