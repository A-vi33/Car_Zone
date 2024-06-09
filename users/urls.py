from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerUser, name="register"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.userProfile, name="profile"),
    path('buy_car/<int:car_id>/', views.buyCar, name='buy_car'),
]
