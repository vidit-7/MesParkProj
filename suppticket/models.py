from django.db import models
from django.contrib.auth.models import User
from merchstore.models import Product, Order
from parktour.models import Tour, Booking
from django.utils import timezone
from django.utils.text import slugify

# import uuid

# Create your models here.

class SupportTicket(models.Model):
    disp_slug = models.SlugField(unique=True, blank=True) 
    user = models.ForeignKey(User, related_name="supp_user", on_delete=models.CASCADE)
    # staff = models.ForeignKey(User, related_name="assigned_staff", on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    booking_sup = models.ForeignKey(Booking, null=True, blank=True, on_delete=models.SET_NULL)
    ord_sup = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    # status = models.CharField(max_length=10, choices=[("open":"Open")],default="open")
    priority_code = models.IntegerField(default=50)
    status_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateField(null=True, blank=True)

    def ticket_priority(self):
        if self.booking_sup != None:
            return "v_high"
        elif self.ord_sup != None:
            return "high"
        else:
            return "normal"
        
    def save(self, *args, **kwargs):
        if self.booking_sup:
            self.priority_code = 150
        elif self.ord_sup:
            self.priority_code = 100

        if not self.disp_slug:
            baseSlug = slugify(self.subject)
            final_slug = baseSlug
            counter = 1
            while SupportTicket.objects.filter(disp_slug=final_slug).exists():
                final_slug = f"{baseSlug}-{counter}"
                counter+=1
            self.disp_slug = final_slug
        super().save(*args, *kwargs)

    def __str__(self):
        return f"ticket: {self.id}-{self.disp_slug}"
        
class SupportMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg_body = models.TextField()
    msg_timestamp = models.DateTimeField(auto_now_add=True)
    # is_read = models.BooleanField(default=False)

    def by_staff(self):
        return self.user.is_staff or self.user.is_superuser
    
    def __str__(self):
        mb = self.msg_body if len(self.msg_body)<20 else self.msg_body[:20]
        return f"ticket {self.ticket.id} - {self.user} - {mb}"