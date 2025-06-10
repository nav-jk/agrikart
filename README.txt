==============================
🚜 FARMHUB BACKEND API DOC
==============================

📦 TECH STACK:
- Django
- Django REST Framework
- Token Authentication

==============================
📁 APPS:
==============================
1. farmer
2. buyer
3. api

==============================
🔐 AUTHENTICATION
==============================

✅ Signup (Buyers only):
[POST] /api/v1/auth/signup/
Payload:
{
  "username": "user1",
  "email": "email@example.com",
  "password": "pass123",
  "phone_number": "9876543210",
  "address": "Buyer address"
}

✅ Signup (Farmers only):
[POST] /api/v1/auth/signup/farmer/
Payload:
{
  "username": "farmer1",
  "email": "farmer@example.com",
  "password": "pass123",
  "phone_number": "9876543210",
  "name": "Farmer Name",
  "address": "Farm address"
}

✅ Login:
[POST] /api/v1/auth/token/
Payload:
{
  "username": "user1",
  "password": "pass123"
}
Response:
{
  "token": "your-token"
}

🔒 All endpoints below require:
Header: Authorization: Token <your-token>


==============================
🚜 FARMER ENDPOINTS
==============================

[GET]    /api/v1/farmer/                  → List all farmers
[POST]   /api/v1/farmer/                  → Create a new farmer
[GET]    /api/v1/farmer/<phone_number>/   → Retrieve specific farmer
[PUT]    /api/v1/farmer/<phone_number>/   → Update farmer
[DELETE] /api/v1/farmer/<phone_number>/   → Delete farmer

→ Nested field: produce (list of produce by the farmer)

==============================
🍅 PRODUCE (NESTED IN FARMER)
==============================
- Each Farmer can have multiple produce items
- Added/Updated via farmer serializer
- No separate endpoint (can be added later)

==============================
🧍‍♂️ BUYER ENDPOINTS
==============================

[GET]    /api/v1/buyer/                   → List all buyers
[POST]   /api/v1/buyer/                   → Create buyer (not used directly, handled via signup)
[GET]    /api/v1/buyer/<phone_number>/    → Retrieve buyer with cart + orders
[PUT]    /api/v1/buyer/<phone_number>/    → Update buyer
[DELETE] /api/v1/buyer/<phone_number>/    → Delete buyer

→ Nested fields: cart, orders


==============================
🛒 CART MANAGEMENT
==============================

[POST] /api/v1/cart/
→ Add item to buyer's cart
Payload:
{
  "produce": 1,
  "quantity": 3
}

[PUT] /api/v1/cart/<int:pk>/
→ Update cart item quantity
Payload:
{
  "quantity": 5
}

[DELETE] /api/v1/cart/<int:pk>/
→ Remove item from cart


==============================
📦 ORDER MANAGEMENT
==============================

[POST] /api/v1/orders/create-from-cart/
→ Create new order from current cart
→ Creates "PENDING" order
→ Deletes all cart items on success
Valid only if there are no other PENDING orders

Response:
{
  "id": 1,
  "status": "PENDING",
  ...
}

[POST] /api/v1/orders/<order_id>/confirm/
→ Confirms payment for an order
→ Only allowed if status == "PENDING"

Response:
{
  "message": "Payment confirmed. Order status updated."
}

Order status values:
- PENDING: Created, waiting for payment
- CONFIRMED: Paid successfully
- CANCELLED: (Future feature)


==============================
🚦 ORDER LIFECYCLE (Frontend Logic)
==============================

1. Add to cart via /api/v1/cart/
2. Call /api/v1/orders/create-from-cart/ → returns new "PENDING" order
3. Complete payment (UI/External)
4. Call /api/v1/orders/<id>/confirm/ to finalize order
5. Order now marked as "CONFIRMED"


==============================
🛡️ SECURITY
==============================
- All routes require Token Auth
- Only the logged-in user can see/modify their data
- Cart and Orders are private per user

==============================
✅ FUTURE IDEAS
==============================
- Stock control on produce
- Webhook-based auto-confirm from payment provider
- Cancel orders
- Separate produce list API
- Add cart item search or duplicate checks

