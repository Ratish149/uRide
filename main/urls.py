from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # pages
    path('', views.home, name='home'),
    path('cars/', views.cars, name='cars'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cardetail/<int:pk>/', views.car_detail, name='car_detail'),


    # Customer profile
    path('profile/',views.customer_profile,name='customer_profile'),
    path('booking/<int:pk>', views.booking, name='booking'),
    path('account-booking/',views.account_booking,name='account_booking'),

    # Change password
    path('change_password/',views.change_password,name='change_password'),
    
    # Reset password
    path('password_reset',auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'),name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),name='password_reset_complete'),



    # Owner Profile
    path('owner-profile/',views.owner_profile,name='owner_profile'),
    path('register-vehicle/',views.register_vehicle,name='register_vehicle'),
    path('your-vehicle/',views.your_vehicle,name='your_vehicle'),
    path('update_vehicle/<int:id>',views.update_vehicle,name='update_vehicle'),
    path('delete_vehicle/<int:id>',views.delete_vehicle,name='delete_vehicle'),
    path('on-rent/',views.on_rent,name='on_rent'),
    path('off_rent/<int:id>',views.off_rent,name='off_rent'),

    # Admin Profile
    path('admin-profile/',views.admin_profile,name='admin_profile'),
    path('vehicle-approve/',views.approve_vehicle,name='vehicle_approve'),
    path('vehicle-approve-detail/<int:id>',views.approve_vehicle_detail,name='vehicle_approve_detail'),
    path('user-approve-detail/<int:id>',views.approve_user_detail,name='user_approve_detail'),
    path('user-approve/',views.approve_user,name='user_approve'),



    # Khalti Payment Integrations
    path('initiate/',views.initkhalti,name="initiate"),
    path('verify/',views.verifyKhalti,name="verify"),

    # Authentication Section
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),


    # Auth Denied Pages
    path('auth_denied/', views.auth_denied, name='auth_denied'),




]