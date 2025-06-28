from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Tour(models.Model):
    tour_type = models.CharField(max_length=255, unique=True)
    desc = models.TextField(null=True, blank=True)
    max_per_day = models.PositiveIntegerField(default=60)
    # vid = models.FileField(null=True, blank=True, upload_to="tour_videos")
    video_url = models.URLField(null=True, blank=True)
    imga = models.ImageField(null=True, blank=True, upload_to='tour_images')
    imgb = models.ImageField(null=True, blank=True, upload_to='tour_images')
    weekday_price = models.DecimalField(max_digits=10, decimal_places=2)
    weekend_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.tour_type
    
    def descShort(self):
        if len(self.desc)>95:
            return self.desc[:95]+'...'
        return self.desc
    
class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uemail = models.EmailField(null=True)
    phone = models.CharField(max_length=20)
    num_visitors = models.PositiveIntegerField()
    booking_date = models.DateField()
    booked_at_date = models.DateTimeField(auto_now_add=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tour.tour_type} on {self.booking_date} - for {self.user} - booked {self.booked_at_date.strftime('on %d/%m/%Y at %H:%M:%S')}"

    def isWeekEnd(self):
        if (self.booking_date.weekday() >= 5):
            return True
        return False
    
    def ticketPrice(self):
        if (self.booking_date.weekday() >= 5):
            return self.tour.weekend_price
        return self.tour.weekday_price

    def totalCost(self):
        if (self.isWeekEnd()):
            return self.num_visitors * self.tour.weekend_price
        return self.num_visitors * self.tour.weekday_price
    
    def isInFuture(self):
        if(self.booking_date>timezone.now().date()):
            return True
        return False

    # def slotsAvailable(self):
    #     current_day_bookings = self.objects.filter(tour=self.tour, booking_date=self.booking_date)
    #     current_day_visitors = 0
    #     for bookings in current_day_bookings:
    #         current_day_visitors += bookings.num_visitors
    #     return self.tour.max_per_day - current_day_visitors