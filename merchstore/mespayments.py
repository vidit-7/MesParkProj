import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(order):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"Order Checkout"},
                    "unit_amount": int(order.ord_total_price() * 100),
                },
                "quantity": 1,
            }
        ],
        success_url = settings.DOMAIN + "/merchandise/confirm-merch-payment/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url  = settings.DOMAIN + "/merchandise/confirm-merch-payment/?session_id={CHECKOUT_SESSION_ID}",
    )

    return session

def retrieve_checkout_session(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    return session