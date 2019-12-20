from django.contrib import admin
from .models import User_details, Cab, Passengers
from django.contrib.auth.models import User
# Register your models here.
class DisplayPassengers(admin.ModelAdmin):
    list_display = ['id', 'user','of_cab'] 

class DisplayCab(admin.ModelAdmin):
    list_display = ['id', 'source', 'destination', 'dep_date_time']

class DisplayUser_details(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'contact_no']

admin.site.register(User_details, DisplayUser_details)
admin.site.register(Cab, DisplayCab)
admin.site.register(Passengers, DisplayPassengers)