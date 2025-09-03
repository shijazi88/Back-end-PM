# payments/views.py
import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Stripe secret key from settings (.env)
stripe.api_key = settings.STRIPE_SECRET_KEY

# Frontend origin (fallback to local dev)
FRONTEND_ORIGIN = getattr(settings, "FRONTEND_ORIGIN", "http://localhost:3000")


@api_view(["POST"])
@permission_classes([AllowAny])
def create_checkout_session(request):
    """
    Creates a Stripe Checkout Session and returns { id, url }.
    After successful payment Stripe will redirect user to:
      <FRONTEND_ORIGIN>/analyze?session_id={CHECKOUT_SESSION_ID}
    On cancel:
      <FRONTEND_ORIGIN>/user-dashboard
    """
    data = request.data or {}

    # Plan & quantity
    plan = (data.get("plan") or "starter").lower()
    try:
        quantity = int(data.get("quantity") or 1)
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, quantity)

    # Pricing in cents
    unit_amount_map = {
        "starter": 1999,
        "pro": 4999,
        "enterprise": 14999,
    }
    unit_amount = unit_amount_map.get(plan, unit_amount_map["starter"])

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            # You can enable promo codes if you want:
            # allow_promotion_codes=True,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"GIS Plan: {plan.title()}"},
                    "unit_amount": unit_amount,
                },
                "quantity": quantity,
            }],
            customer_email=data.get("email") or None,
            success_url=f"{FRONTEND_ORIGIN}/analyze?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_ORIGIN}/user-dashboard",
            metadata={
                "full_name": data.get("full_name", ""),
                "company": data.get("company", ""),
                "phone": data.get("phone", ""),
                "notes": data.get("notes", ""),
                "plan": plan,
                "quantity": str(quantity),
                # لو حابة تضيفي analysis_id فيما بعد:
                # "analysis_id": data.get("analysis_id", ""),
            },
        )

        # Return both id (for redirectToCheckout) and url (direct redirect)
        return Response({"id": session.id, "url": session.url}, status=status.HTTP_200_OK)

    except stripe.error.AuthenticationError:
        return Response(
            {"error": "Invalid Stripe API key (check STRIPE_SECRET_KEY)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
