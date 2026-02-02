import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(booking):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"Tour Booking"},
                    "order_amount": int(booking.total_cost * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=(
            settings.DOMAIN
            + "/payment/process/?session_id={CHECKOUT_SESSION_ID}"
        ),
        cancel_url=settings.DOMAIN + "/payment/cancel/",
    )

    return session