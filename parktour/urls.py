from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tourHome, name="parkTourHome"),
    path('explore-tour/<str:pk>', views.tourExplore, name="parkTourExplore"),
    path('book-tour/<str:pk>', views.tourBook, name="parkTourBooking"),
    path('confirm-tour-booking/<str:booking_id>', views.tourBookConfirm, name="parkTourBookConfirm"),
    path('confirm-booking-payment/', views.confirmBookingPayment, name='confirmBookingPayment'),
    path('check-booking-status/', views.tourCheckStatus, name="parkTourCheckBookingStatus"),
    path('tour-bookings/', views.tourBookings, name="parkTourBookings"),
]