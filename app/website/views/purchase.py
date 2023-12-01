import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from website.models import OrderDish, Order, OrderStatus
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

class Purchase:
    @login_required
    def post(request, *args, **kwargs):
        order_data = OrderDish.objects \
                    .select_related('order', 'dish', 'status') \
                    .filter(order_id=kwargs["order_id"])

        items_to_purchase = []

        for order_dish in order_data:
            item = {
                "price_data": {
                    "currency": "mxn",
                    "unit_amount": int(int(order_dish.dish.price) * 100),
                    "product_data": {
                        "name": order_dish.dish.name,
                        "description": order_dish.dish.description,
                        "metadata": {
                            "product_id": order_dish.dish.id
                        },
                    },
                },
                "quantity": 1,
            }
            items_to_purchase.append(item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items_to_purchase,
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
            payment_intent_data={
                "metadata": {
                    "order_id": order_data.first().order.id,
                    "user_id": order_data.first().order.customer_id,
                }
            }
        )
        
        return redirect(checkout_session.url)

    @login_required
    def success(request):
        order = Order.objects.filter(customer_id=request.user.id).latest("created_at")
        request.session["order_id"] = order.id
        request.session["order_count"] = 0
        return render(request, "website/purchase/success.html")

    @login_required
    def cancel(request):
        return render(request, "website/purchase/cancel.html")

class StripeWebhook:
    @csrf_exempt
    def post(request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.headers.get('Stripe-Signature', None)
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            print(f"Error (invalid payload): {e}")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            print(f"Error (invalid signature): {e}")
            return HttpResponse(status=400)

        if event["type"] == "payment_intent.succeeded":
            print("Payment successful")

            event_metadata = event["data"]["object"]["metadata"]

            order = Order.objects.get(id=int(event_metadata.get("order_id")))
            order.status_id = 5
            order.save()

            user = User.objects.get(id=int(event_metadata.get("user_id")))

            status = OrderStatus.objects.get(id=2)

            new_order = Order.objects.create(customer=user, status=status)

        return HttpResponse(status=200)
