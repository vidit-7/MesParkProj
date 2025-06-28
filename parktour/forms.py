from django import forms
from django.utils import timezone
from parktour.models import Tour, Booking

from datetime import datetime

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'

    def clean_video_url(self):
        url = self.cleaned_data.get('video_url')
        
        if not url or str(url).strip()=="":
            return None
        url = str(url).strip()

        valid_prefixes = [
            'https://www.youtube.com/watch?v=',
            'https://youtu.be/',
            'https://www.youtube.com/embed/',
        ]

        if not url.startswith('https://'):
            url = 'https://'+url
        
        url_match = False
        for prefix in valid_prefixes:
            if url.startswith(prefix):
                url_match = True
                break
        
        if not url_match:
            raise forms.ValidationError("Please enter a valid YouTube video URL.")

        # Convert to embed format
        video_id = None
        if '/watch?v=' in url:
            url = url.split('watch?v=')[-1]
            video_id = url.split('&')[0]
        elif '/youtu.be/' in url:
            video_id = url.split('/')[-1]
        elif '/embed/' in url:
            return url

        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'

        raise forms.ValidationError("Unable to extract YouTube video ID.")
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['phone','uemail','num_visitors','booking_date']

        labels = {
            'phone': 'Your phone number',
            'uemail': 'Your email address',
            'num_visitors': 'How many people will be visiting? You can buy upto 12 tickets.',
            'booking_date': 'Pick a date for your visit to the park!',
        }
        widgets = {
            'phone' : forms.TextInput(attrs={'class':'form-control fs-sm-5','placeholder':'Your phone number...'}),
            'uemail' : forms.EmailInput(attrs={'class':'form-control fs-sm-5','placeholder':'Your email address...'}), #,'required':'true'
            # 'num_visitors': forms.Select(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),
            #                                       (6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10'),
            #                                       (11,'11'),(12,'12'),]),
            'num_visitors': forms.Select(choices=[(i,str(i)) for i in range(1,13)]),
            'booking_date': forms.DateInput(attrs={'class':'form-control fs-sm-5', 'type': 'date'}) 
        }

    # to get tuser as kwargs
    def __init__(self, *args, **kwargs):
        self.fv_user = kwargs.pop('fv_user', None)
        self.fv_tour = kwargs.pop('fv_tour', None)
        # print("userid ",self.fv_user)
        # print("tourid ",self.fv_tour)
        super().__init__(*args, **kwargs)

    def clean_booking_date(self):
        tdate = self.cleaned_data.get('booking_date')
        if(tdate <= timezone.now().date()):
            raise forms.ValidationError("Please select a future date.")
        
        if self.fv_user and tdate:
            if Booking.objects.filter(user=self.fv_user, booking_date=tdate).exists():
                raise forms.ValidationError("You already have a tour booked for the selected day. Please choose a different date.")
            
        return tdate

    def clean_num_visitors(self):
        num_wish = self.cleaned_data.get('num_visitors')
        if (num_wish<1 or num_wish>12):
            raise forms.ValidationError("Please select upto 12 tickets only.")
        
        return num_wish

    def clean(self):
        cleaned_data = super().clean()

        tdate = cleaned_data.get('booking_date')
        num_wish = cleaned_data.get('num_visitors')

        if self.fv_tour and tdate and num_wish:
            existing_day_bookings = Booking.objects.filter(tour=self.fv_tour, booking_date=tdate)
            # booked_total = sum(b.num_visitors for b in existing)
            already_attending_visitors = 0
            for booking in existing_day_bookings:
                already_attending_visitors += booking.num_visitors

            available_tickets = self.fv_tour.max_per_day - already_attending_visitors
            # print("av t",available_tickets)
            # if total_visitors + num_wish > self.fv_tour.max_per_day:
            if num_wish > available_tickets:
                raise forms.ValidationError("Not enough slots available on this date.")
            
        return cleaned_data
