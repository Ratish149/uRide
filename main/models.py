from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CarModel(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
    
    def save(self,*args, **kwargs):
        self.name=self.name.capitalize()
        super().save(*args, **kwargs)
class CarType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
    
    def save(self,*args, **kwargs):
        self.name=self.name.capitalize()
        super().save(*args, **kwargs)

class GearType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
    
    def save(self,*args, **kwargs):
        self.name=self.name.capitalize()
        super().save(*args, **kwargs)

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)

class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=20)
    vehicle_description = models.TextField()
    vehicle_number = models.CharField(max_length=10)
    vehicle_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    vehicle_gear = models.ForeignKey(GearType, on_delete=models.CASCADE, null=True)
    vehicle_color = models.CharField(max_length=20)
    vehicle_front_image = models.ImageField(upload_to='vehicle/vehicle_images/' )
    vehicle_right_image = models.ImageField(upload_to='vehicle/vehicle_images/')
    vehicle_left_image = models.ImageField(upload_to='vehicle/vehicle_images/')
    vehicle_back_image = models.ImageField(upload_to='vehicle/vehicle_images/')
    vehicle_location = models.CharField(max_length=200)
    vehicle_seat = models.IntegerField()
    uploaded_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_by')
    rented_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_by', null=True,blank=True)
    price_per_day = models.IntegerField()
    isDeleted=models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def _str_(self):
        return f'{self.vehicle_name} - {self.vehicle_model}'
    
    def save(self,*args, **kwargs):
        self.vehicle_name=self.vehicle_name.capitalize()
        self.vehicle_color=self.vehicle_color.capitalize()
        self.vehicle_location=self.vehicle_location.capitalize()

        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    full_name = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    licence_picture = models.ImageField(upload_to='licence_pictures/', blank=True, null=True)

    def _str_(self):
        return self.user.username

class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_date = models.DateField(auto_now=False, auto_now_add=False)
    return_date = models.DateField(auto_now=False, auto_now_add=False)
    amount = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Ongoing')
    # isPaid = models.BooleanField(default=False)

class BookingTransaction(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id=models.CharField(max_length=100)
    amount = models.IntegerField()
    # isPaid = models.BooleanField(default=False)
    rented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id


class Review(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.vehicle.vehicle_name}'