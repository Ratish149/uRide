from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
from .decorators import admin_only, customer_only, owner_only
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm,VehicleForm,ReviewForm,BookingForm
from .models import *


# WEBSITE PAGES
def home(request):
    vehicle=Vehicle.objects.filter(available=True,isDeleted=False)

    context={
        'vehicle':vehicle
    }
    return render(request, 'index.html',context)

# Display all cars including search function and filter function
def cars(request):
    vehicles = Vehicle.objects.filter(available=True,isDeleted=False,approved=True)
    searched_text=request.GET.get('searched_text')
    if searched_text:
        vehicles = Vehicle.objects.filter(vehicle_name__icontains=searched_text,available=True,approved=True)

    selected_vehicle_types = request.GET.getlist('vehicle_type')
    selected_vehicle_models = request.GET.getlist('vehicle_model')
    selected_gear_types = request.GET.getlist('gear_type')
    selected_car_seats = request.GET.getlist('car_seat')
    
    vehicle_types = CarType.objects.all()
    vehicle_models = CarModel.objects.all()
    gear_types = GearType.objects.all()  
    
    if selected_vehicle_types:
        vehicles = Vehicle.objects.filter(vehicle_type__id__in=selected_vehicle_types,available=True,isDeleted=False,approved=True)
    if selected_vehicle_models:
        vehicles = Vehicle.objects.filter(vehicle_model__id__in=selected_vehicle_models,available=True,isDeleted=False,approved=True)
    if selected_gear_types:
        vehicles = Vehicle.objects.filter(vehicle_gear__id__in=selected_gear_types,available=True,isDeleted=False,approved=True)
    if selected_car_seats:
        seat_filters = [int(seat.split('_')[-1]) for seat in selected_car_seats if seat != 'car_seat_6_plus']
        if 'car_seat_6_plus' in selected_car_seats:
            vehicles = vehicles.filter(vehicle_seat__gt=6,available=True,isDeleted=False,approved=True)
        else:
            vehicles = vehicles.filter(vehicle_seat__in=seat_filters,available=True,isDeleted=False,approved=True)

    context = {
        'vehicle_types': vehicle_types,
        'vehicle_models': vehicle_models,
        'gear_types': gear_types,
        'vehicles': vehicles,
        'selected_vehicle_types': list(map(int, selected_vehicle_types)),
        'selected_vehicle_models': list(map(int, selected_vehicle_models)),
        'selected_gear_types': list(map(int, selected_gear_types)),
        'selected_car_seats': selected_car_seats,
    }
    return render(request, 'cars.html',context)

# Display single car Detail
def car_detail(request,pk):
    data = Vehicle.objects.get(id=pk)
    reviews = data.reviews.all()

    if request.method == 'POST' and request.user.is_customer:
        form=ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.vehicle = data
            review.save()
            return redirect('car_detail', pk=data.id)

    else:
        form = ReviewForm()

    context ={
        'data':data,
        'reviews':reviews,
        'form':form,
        'range':range(1,6)
    }
    return render(request, 'car-single.html',context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        date=datetime.now()

        context={
            'name':name,
            'email':email,
            'phone':phone,
            'message':message,
            'date':date
        }
        subject="Thank you for contacting us"
        message=render_to_string('message.html',context)
        from_email='bdevil149@gmail.com'
        recipient_list=[email,'ratish.shakya149@gmail.com']
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, 'Thank you for contacting us. We will get back to you shortly.')
    
        return redirect('contact')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

# WEBSITE PAGES END

# CUSTOMER PAGES
# Display customer profile and Update profile
@customer_only
def customer_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('customer_profile')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'pages/customer/profile.html', context)

# Display booking page
@customer_only
def booking(request,pk):
    vehicle=Vehicle.objects.get(id=pk)
    bookingform = BookingForm()
    context={
        'vehicle':vehicle,
        'booking':bookingform
    }
    return render(request, 'pages/customer/booking.html',context)

@customer_only
def account_booking(request):
    vehicle=Vehicle.objects.filter(rented_by=request.user,isDeleted=False,approved=True)
    booking = Booking.objects.filter(user=request.user,status="Ongoing")
    context={
        'vehicle':booking,
        'profile': request.user.profile
    }
    return render(request, 'pages/customer/account-booking.html',context)


# CUSTOMER PAGES END

# OWNER PAGES
# Display owner profile and Update profile
@owner_only
def owner_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('owner_profile')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }
      
    return render(request, 'pages/owner/owner_profile.html',context)

# Owner Register vehicle section
@owner_only
def register_vehicle(request):
    if request.method == 'POST':
        form=VehicleForm(request.POST,request.FILES)
        if form.is_valid():
            vehicle=form.save(commit=False)
            vehicle.uploaded_by = request.user
            vehicle.save()  
            return redirect('owner_profile')
    else:
        form = VehicleForm()
    context={
         'profile':request.user.profile,
         'form':form
    }
    return render(request,'pages/owner/register_vehicle.html',context)

# Display Registered vehicle
@owner_only
def your_vehicle(request):
    vehicle=Vehicle.objects.filter(uploaded_by=request.user,isDeleted=False,approved=True)
    data=Vehicle.objects.filter(uploaded_by=request.user,approved=False,isDeleted=False)
    context={
         'vehicle':vehicle,
         'data':data,
         'profile': request.user.profile
    }
    return render(request, 'pages/owner/your_vehicle.html',context)

# Update vehicle information
@owner_only
def update_vehicle(request,id):
    vehicle=Vehicle.objects.get(id=id)
    
    if request.method == 'POST':
        form=VehicleForm(request.POST,request.FILES,instance=vehicle)
        if form.is_valid():
            form.save()  
            return redirect('your_vehicle')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request,'pages/owner/update_vehicle.html',{'form':form,'profile':request.user.profile})

# Delete vehicle
@owner_only
def delete_vehicle(request,id):
    vehicle=Vehicle.objects.get(id=id)
    vehicle.isDeleted=True
    vehicle.save()
    return redirect('your_vehicle')

@owner_only
def on_rent(request):
    vehicle=Vehicle.objects.filter(uploaded_by=request.user,available=False,isDeleted=False)

    context = {
        'vehicle': vehicle,
        'profile': request.user.profile,
    }
    return render(request, 'pages/owner/on_rent.html', context)

@owner_only
def off_rent(request,id):
    if request.method=='POST':
        vehicle=Vehicle.objects.get(id=id,available=False)
        # booking=Booking.objects.get(uploaded_by=request.user)
        vehicle.available=True
        booking.status="Completed"
        vehicle.save()
    return redirect('on_rent')


# OWNER PAGES END


# ADMIN PAGE

@admin_only
def admin_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('admin_profile')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'pages/admin/admin_profile.html',context)

@admin_only
def approve_vehicle(request):
    vehicles=Vehicle.objects.filter(approved=False,isDeleted=False)
    approved_vehicles=Vehicle.objects.filter(approved=True,isDeleted=False)

    context={
        'vehicles':vehicles,
        'approved_vehicles':approved_vehicles,
        'profile': request.user.profile,

    }
    return render(request, 'pages/admin/vehicle_approve.html',context)

@admin_only
def approve_vehicle_detail(request,id):
    vehicle=Vehicle.objects.get(id=id)

    if request.method == 'POST':
        vehicle=get_object_or_404(Vehicle,id=id)
        vehicle.approved=True
        vehicle.save()
        return redirect('vehicle_approve')
    context={
        'vehicle':vehicle,
        
    }
    return render(request, 'pages/admin/approve_vehicle_detail.html',context)

def approve_user(request):
    user=User.objects.filter(approved=False)

    context={
        'user':user,
        'profile': request.user.profile,

    }
    return render(request, 'pages/admin/user_approve.html',context)

# ADMIN PAGE END


# AUTHENTICATION PAGES
# Login user based on its role
def log_in(request):
    if request.method == 'POST':
        data=request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request,username=username, password=password)
    
        if not User.objects.filter(username=username).exists():
                messages.error(request,"Username doesn't exist")

        elif user is not None and user.is_admin:
                login(request, user)
                return redirect('admin_profile')
        elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer_profile')
        elif user is not None and user.is_owner:
                login(request, user)
                return redirect('owner_profile')
        else:
                messages.error(request,"Try again!")
                return redirect('login_view')
        
    return render(request, 'auth/login.html')

# Register new user
def register(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,'You Have Successfully Registered!!')
            return redirect('login')
        else:
            messages.error(request,'Invalid Form')
    else:
        form=SignUpForm()
    return render(request,'auth/register.html',{'form':form})


# Logout user
def log_out(request):
    logout(request)
    return redirect('login')


# AUTHENTICATION PAGES END

# KHALTI PAYMENT INTEGRATION
# Initiate khalti payment
@csrf_exempt
def initkhalti(request):
    if request.method=='POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        return_url = "http://127.0.0.1:8000/verify/"
        
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        amount=request.POST.get('total_price')
        message=request.POST.get('message')
        vehicle_id=request.POST.get('vehicle_id')
        owned_by=request.POST.get('owned_by')
        pickup_date=request.POST.get('pickup_date')
        return_date=request.POST.get('return_date')
        purchase_order_id=request.POST.get('vehicle_id')
        purchase_order_name=request.POST.get('vehicle_name')

        transaction_id=str(uuid4())

        print(name,email,phone,amount,message,vehicle_id,owned_by,purchase_order_id,purchase_order_name)
        print(return_url)

        payload = json.dumps({
            "return_url": return_url,
            "website_url": "http://127.0.0.1:8000/",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "transaction_id": transaction_id,
            "customer_info": {
            "name": name,
            "email": email,
            "phone": phone,
            }
        })
        headers = {
            'Authorization': 'key 1ecf6a98463d4ecf8e77ba8a9bdd16d0',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        new_res=json.loads(response.text)
        print(new_res)
    
        if response.status_code == 200 and 'payment_url' in new_res:
            vehicle=Vehicle.objects.get(id=purchase_order_id)
            Booking.objects.create(
                vehicle=vehicle,
                user=request.user,
                pickup_date=pickup_date,
                return_date=return_date,
                amount=amount,
                status='Ongoing'
            )
            return redirect(new_res['payment_url'])
        else:
            return JsonResponse({'error': 'Failed to initiate payment', 'details': new_res}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Verify khalti payment and save to the model
@csrf_exempt
def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"

    if request.method == 'GET':
        pidx=request.GET.get('pidx')

        headers = {
            'Authorization': 'key 1ecf6a98463d4ecf8e77ba8a9bdd16d0',
            'Content-Type': 'application/json',
        }

        transaction_id=request.GET.get('transaction_id')
        purchase_order_id=request.GET.get('purchase_order_id')

        payload= json.dumps({
            "pidx": pidx
        })

        response = requests.request("POST", url, headers=headers, data=payload)
  
        new_res=json.loads(response.text)
        print(new_res)

        if new_res['status'] == 'Completed':
            vehicle=Vehicle.objects.get(id=purchase_order_id)
            vehicle.available=False
            vehicle.rented_by=request.user
            vehicle.save()

            booking = Booking.objects.get(user=request.user)
            booking.status="Completed"

            BookingTransaction.objects.create(
                vehicle=vehicle,
                transaction_id=transaction_id,
                amount=new_res['total_amount'],
                user=vehicle.rented_by
            )
            date=datetime.now()
            # subject="Vehicle Rented"
            # message=f"Your vehicle {vehicle.vehicle_name} has been successfully rented by {request.user.username} . Thank you for using our service."
            # from_email='bdevil149@gmail.com'
            # recipient_list=[vehicle.uploaded_by.email,'ratish.shakya149@gmail.com']
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            subject="Vehicle Rental Confirmation"
            message=render_to_string('rent_confirmation.html',{'vehicle':vehicle,'date':date,'amount':new_res['total_amount'],'user':request.user})
            from_email='bdevil149@gmail.com'
            recipient_list=[request.user.email,vehicle.uploaded_by.email,'ratish.shakya149@gmail.com']
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('cars')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)