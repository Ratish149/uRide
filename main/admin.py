from django.contrib import admin

from .models import *
# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display=('vehicle_name','uploaded_by','vehicle_model','price_per_day','vehicle_front_image','approved')
    list_filter=('approved',)
    actions=['approve_vehicle']

    def approve_vehicle(self,request,queryset):
        queryset.update(approved=True)

    approve_vehicle.short_description="Approve Selected Vehicle"

admin.site.register(Vehicle,VehicleAdmin)
admin.site.register(User)
admin.site.register(CarType)
admin.site.register(CarModel)
admin.site.register(GearType)
# admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','full_name','phone_number','profile_picture','licence_picture')

@admin.register(BookingTransaction)
class BookingTransactionAdmin(admin.ModelAdmin):
    list_display=('vehicle','user','amount','transaction_id','rented_at')
    list_filter=('rented_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=('vehicle','user','rating','comment','created_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('vehicle','user','pickup_date','return_date','amount','status')




