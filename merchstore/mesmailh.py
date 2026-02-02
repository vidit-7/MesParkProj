from django.core.mail import send_mail, send_mass_mail

def merchOrderConfirmationMail(user, order):
    if order.uemail != "":
        send_mail(
            subject=f"Confirmation of {order}",
            message=f"Greetings {user.first_name},\n\n\tThis is a confirmation email for your order that has been successfully booked on {order.created_at}. The total amount of the order placed is ${order.ord_total_price()} for {order.total_products()} products. The net quantity is {order.total_qty()}. Payment method {order.payment_status}.\nThank you for shopping with us!\n\nRegards,\nMesozoic Park Admin\n\nP.S. This is a system generated mail, please do not reply. For any questions, contact us at link.",
            from_email="mesparkadmin@ingen.inc",
            recipient_list=[order.uemail],
            fail_silently=False
        )