from django.urls import path
from . import views


urlpatterns = [
    # path('register/', views.registerUser, name="register"),
    path('register/', views.UserRegisterView.as_view(), name="register"),
    # path('login/', views.loginUser, name="login"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.userProfile, name="profile"),
    path('save-address/', views.save_address, name='save_address'),
    path('change_password/', views.CustomPasswordChangeView.as_view(), name="change_password"),
    path('update_profile/', views.updateProfile, name="update_profile"),
    path('buy_car/<int:car_id>/', views.buyCar, name='buy_car'),
    path('payment-handler/', views.paymentHandler, name='payment_handler'),
    path('initiate-payment/', views.initiatePayment, name='initiate_payment'),
    path('payment-success/', views.paymentsuccess, name='payment_success'),
    path('add-delivery-address/', views.addDeliveryAddress, name='add_delivery_address'),

]
