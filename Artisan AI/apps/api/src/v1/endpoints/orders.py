# endpoints/orders.py

# Purpose: Carts, checkout, webhooks.
# Routes: create cart, add/remove item, POST /checkout (create payment intent), webhook receiver.
# Uses: services.payment_service, repos.firestore.