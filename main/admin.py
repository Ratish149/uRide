from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Vehicle)
admin.site.register(User)
admin.site.register(CarType)
admin.site.register(CarModel)
admin.site.register(GearType)
admin.site.register(Profile)
admin.site.register(BookingTransaction)
admin.site.register(Review)


