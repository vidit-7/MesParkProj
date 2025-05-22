from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Extending user model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, default="No information.")
    pic = models.ImageField(blank=True, default='defaults/defaultuser.png', upload_to='profile_pics/')
    phone = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"Profile for: {self.user.username}"
    


