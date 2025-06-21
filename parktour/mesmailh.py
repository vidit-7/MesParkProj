from django.core.mail import send_mail, send_mass_mail

def tourBookingConfirmationMail(user, booking):
    if booking.uemail != "":
        send_mail(
            subject=f"Booking for {booking.tour} tour confirmed on {booking.booking_date}.",
            message=f"Greetings {user.first_name},\n\n\tThis is a confirmation email for your park tour successfully booked for {booking.num_visitors} visitors on {booking.booking_date}. The total cost of the tour is ${booking.total_cost}.\nWe hope to see you soon!\n\nRegards,\nMesozoic Park Admin\n\nP.S. This is a system generated mail, please do not reply. For any questions, contact us at link.",
            from_email="mesparkadmin@ingen.inc",
            recipient_list=[booking.uemail],
            fail_silently=False
        )