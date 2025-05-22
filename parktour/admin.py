from django.contrib import admin
from parktour.models import Tour, Booking
from parktour.forms import TourForm

# Register your models here.

class TourAdmin(admin.ModelAdmin):
    form = TourForm

admin.site.register(Tour, TourAdmin)
admin.site.register(Booking)