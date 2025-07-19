from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from parktour.models import Tour, Booking
from parktour.forms import BookingForm

from parktour.mesmailh import tourBookingConfirmationMail

import json
from datetime import datetime
# Create your views here.

def tourHome(request):
    tours = Tour.objects.all().order_by('weekday_price', 'weekend_price')
    context = {'tours':tours}
    return render(request, 'parktour/tours.html', context)

def tourExplore(request, pk):
    tour = Tour.objects.get(id=pk)
    context = {'tour': tour}
    return render(request, 'parktour/explore-tour.html', context)
    
@login_required(login_url="centBaseLoginUser")
def tourBook(request, pk):
    try:
        tour = Tour.objects.get(id=pk)
    except:
        return HttpResponse("Invalid tour")

    if request.method == "POST":
        booking_form = BookingForm(request.POST, fv_user=request.user, fv_tour=tour)

        if 'confirm-final' in request.POST:
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.tour = tour
                booking.total_cost = booking.totalCost()
                
                booking.save()
                messages.success(request, "Your tour has been booked successfully. We hope to see you soon!")

                tourBookingConfirmationMail(request.user, booking)

                return redirect("parkTourBookings")
            else:
                messages.error(request, "There was an error booking your tour. You may try again.")
                return render(request, 'parktour/book-tour.html', {"tour": tour, "booking_form": booking_form})
            
        else:
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.tour = tour
                booking.total_cost = booking.totalCost()
              
                b_date = booking.booking_date

                context = {
                    "tour": tour,
                    "ticket_price": booking.ticketPrice(),
                    "num_tickets": booking.num_visitors,
                    "booking_cost": booking.totalCost(),
                    "b_uemail": booking.uemail,
                    "b_phone": booking.phone,
                    "b_date": b_date,
                    "booking_form": booking_form
                }
                return render(request, 'parktour/confirm-booking.html', context)
            else:
                return render(request, 'parktour/book-tour.html', {"tour": tour, "booking_form": booking_form})

    initial_form_fields = {'phone': request.user.profile.phone, 'uemail': request.user.email}
    booking_form = BookingForm(initial=initial_form_fields, fv_user=request.user, fv_tour=tour)
    context = {"tour": tour, "booking_form": booking_form}
    return render(request, 'parktour/book-tour.html', context)

@login_required(login_url="centBaseLoginUser")
def tourCheckStatus(request):
    if request.method == "POST":
        # print(data['bookDate'])
        try:
            data = json.loads(request.body)
            tourId = data['tourId']
            numVis = int(data['numVis'])
            bookDate = datetime.strptime(data['bookDate'], "%Y-%m-%d").date()
            purpose = data['purpose']
        except:
            return JsonResponse({'success': False, "show_message": "Error"})

        # check future date
        if(bookDate<=timezone.now().date()):
            return JsonResponse({'success': False, 'show_message': 'Please select a future date.'})
        
        # check already booked tours
        if Booking.objects.filter(user=request.user, booking_date=bookDate).exists():
            return JsonResponse({'success': False, 'show_message': f'You already have a tour booked on {bookDate}'})
        # check num of slots
        try:
            fetch_tour = Tour.objects.get(id=tourId)
        except:
            return JsonResponse({'success': False, "show_message": "Error"})
        
        current_day_bookings = Booking.objects.filter(tour=fetch_tour, booking_date=bookDate)

        current_day_visitors = 0
        for booking in current_day_bookings:
            current_day_visitors += booking.num_visitors
            
        available_slots = fetch_tour.max_per_day - current_day_visitors
        
        if(available_slots >= numVis):
            return JsonResponse({"success": True, "show_message": f"You can book a tour for {numVis} visitor(s) on {bookDate}."})
        else:
            if available_slots > 0:
                show_message = f"Only {available_slots} slot(s) are available on {bookDate}."
            else:
                show_message = f"No slots available on {bookDate}. Please choose another date."
            return JsonResponse({"success": False, "show_message": show_message})

    else:
        return HttpResponse("Invalid request")


@login_required(login_url="centBaseLoginUser")
def tourBookings(request):

    bookings = Booking.objects.filter(user=request.user).order_by('booking_date','-booked_at_date')
    context = {'bookings': bookings, 'booking_count': bookings.count()}
    return render(request, 'parktour/bookings.html', context)