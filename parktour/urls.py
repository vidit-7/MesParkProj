from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tourHome, name="parkTourHome"),
    path('explore-tour/<str:pk>', views.tourExplore, name="parkTourExplore"),
    path('confirm-and-book-tour/<str:pk>', views.tourBook, name="parkTourBooking"),
    path('check-booking-status/', views.tourCheckStatus, name="parkTourCheckBookingStatus"),
    path('tour-bookings/', views.tourBookings, name="parkTourBookings"),
]