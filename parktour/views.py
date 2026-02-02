from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from parktour.models import Tour, Booking
from parktour.forms import BookingForm

from parktour.mesmailh import tourBookingConfirmationMail
from parktour.mespayments import create_checkout_session, retrieve_checkout_session

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
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.total_cost = booking.totalCost()
            
            booking.save()

            b_date = booking.booking_date

            return redirect('parkTourBookConfirm', booking_id=booking.id)
        else:
            return render(request, 'parktour/book_tour.html', {"tour": tour, "booking_form": booking_form})

    initial_form_fields = {'phone': request.user.profile.phone, 'uemail': request.user.email}
    booking_form = BookingForm(initial=initial_form_fields, fv_user=request.user, fv_tour=tour)
    context = {"tour": tour, "booking_form": booking_form}
    return render(request, 'parktour/book_tour.html', context)

@login_required
def tourBookConfirm(request, booking_id):
    # booking_id_req = request.POST.get('booking-id')
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user, booking_stage="DRAFT")
    except:
        return HttpResponse("Booking does not exist")
    
    if(booking.booking_date <= timezone.now().date()):
        messages.error(request, f"Expired. Booking can not be confirmed.")
        return redirect("parkTourHome")

    if Booking.objects.filter(user=request.user, booking_date=booking.booking_date, booking_stage="CONFIRMED").exists():
        messages.error(request, f"You have another booking confirmed on {booking.booking_date} already.")
        return redirect("parkTourHome")
    
    existing_day_bookings = Booking.objects.filter(tour=booking.tour, booking_date=booking.booking_date, booking_stage="CONFIRMED")
    already_attending_visitors = 0
    for bk in existing_day_bookings:
        already_attending_visitors += bk.num_visitors
    available_tickets = booking.tour.max_per_day - already_attending_visitors
    if booking.num_visitors > available_tickets:
        messages.error(request, f"Enough slots not available on {booking.booking_date}. Please try to make a new booking.")
        return redirect("parkTourHome")
    
    if request.method == 'POST':
        if 'confirm-final' in request.POST and 'payment_method' in request.POST:
            booking.booking_stage = "CONFIRMED"
            booking.save(update_fields=['booking_stage'])

            if not settings.STRIPE_KEYS_SET:
                messages.success(request, "Your tour has been booked successfully. We hope to see you soon!")
                tourBookingConfirmationMail(request.user, booking)
                return redirect("parkTourBookings")
            else:
                payment_method = request.POST.get('payment_method')
                if payment_method == 'method_stripe':
                    session = create_checkout_session(booking)
                    booking.stripe_session_id = session.id
                    booking.save(update_fields=['stripe_session_id'])
                    return redirect(session.url)
                else:
                    messages.success(request, "Your tour has been booked successfully. We hope to see you soon!")
                    tourBookingConfirmationMail(request.user, booking)
                return redirect("parkTourBookings")
    else:
        context = {
            "tour": booking.tour,
            "ticket_price": booking.ticketPrice(),
            "num_tickets": booking.num_visitors,
            "booking_cost": booking.totalCost(),
            "b_uemail": booking.uemail,
            "b_phone": booking.phone,
            "b_date": booking.booking_date,
            }
        return render(request, 'parktour/confirm_booking.html', context)

@login_required
def confirmBookingPayment(request):
    if not settings.STRIPE_KEYS_SET:
        return HttpResponse("Stripe not configured")

    session_id = request.GET.get('session_id')
    if not session_id:
        return HttpResponse("No session id provided")

    session = retrieve_checkout_session(session_id)
    try:
        tourBooking = Booking.objects.get(stripe_session_id=session_id, user=request.user, booking_stage="CONFIRMED")
    except:
        return HttpResponse("BOOKING not found")

    if tourBooking.payment_status == 'PAID':
        return redirect('parkTourBookings')

    if session.payment_status == 'paid':
        messages.success(request,"Payment Successful. Your tour has been booked.")
        tourBooking.payment_status = 'PAID'
    else:
        messages.info(request, "Payment Failed. Your tour has been booked and payment can be made on arrival. Feel free to contact us for any help.")

    tourBookingConfirmationMail(request.user, tourBooking)
    tourBooking.save(update_fields=['payment_status'])
    return redirect('parkTourBookings')

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
        if Booking.objects.filter(user=request.user, booking_date=bookDate, booking_stage="CONFIRMED").exists():
            return JsonResponse({'success': False, 'show_message': f'You already have a tour booked on {bookDate}'})
        # check num of slots
        try:
            fetch_tour = Tour.objects.get(id=tourId)
        except:
            return JsonResponse({'success': False, "show_message": "Error"})
        
        current_day_bookings = Booking.objects.filter(tour=fetch_tour, booking_date=bookDate, booking_stage="CONFIRMED")

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

    bookings = Booking.objects.filter(user=request.user, booking_stage="CONFIRMED").order_by('booking_date','-booked_at_date')
    context = {'bookings': bookings, 'booking_count': bookings.count()}
    return render(request, 'parktour/bookings.html', context)