from django.urls import path
from . import views

urlpatterns = [
    # pages
    path('', views.home, name='home'),
    path('cars/', views.cars, name='cars'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cardetail/<int:pk>/', views.car_detail, name='car_detail'),
    path('booking/<int:pk>', views.booking, name='booking'),

    path('profile/',views.customer_profile,name='customer_profile'),
    path('account-booking/',views.account_booking,name='account_booking'),


    path('owner-profile/',views.owner_profile,name='owner_profile'),
    path('register-vehicle/',views.register_vehicle,name='register_vehicle'),
    path('your-vehicle/',views.your_vehicle,name='your_vehicle'),
    path('update_vehicle/<int:id>',views.update_vehicle,name='update_vehicle'),
    path('delete_vehicle/<int:id>',views.delete_vehicle,name='delete_vehicle'),

    path('initiate/',views.initkhalti,name="initiate"),
    path('verify/',views.verifyKhalti,name="verify"),

    # auth
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('register-profile-detail/', views.reg_profile_detail, name='reg_profile_detail'),
    path('logout/', views.log_out, name='logout'),




]