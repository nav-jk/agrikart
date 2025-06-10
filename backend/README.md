# 🚜 AgriKart.ai Backend API

## 📦 TECH STACK
- Django
- Django REST Framework
- Token Authentication

---

## 📁 APPS

- `farmer`
- `buyer`
- `api`

---

## 🔐 AUTHENTICATION

### ✅ Buyer Signup
**POST** `/api/v1/auth/signup/`

```json
{
  "username": "user1",
  "email": "email@example.com",
  "password": "pass123",
  "phone_number": "9876543210",
  "address": "Buyer address"
}
```

---

### ✅ Farmer Signup (for WhatsApp onboarding later)
**POST** `/api/v1/auth/signup/farmer/`

```json
{
  "username": "farmer1",
  "email": "farmer@example.com",
  "password": "pass123",
  "phone_number": "9876543210",
  "name": "Farmer Name",
  "address": "Farm address"
}
```

---

### ✅ Login (All Users)
**POST** `/api/v1/auth/token/`

```json
{
  "username": "user1",
  "password": "pass123"
}
```

➡️ Returns:
```json
{
  "token": "your-auth-token"
}
```

> All protected routes require:
`Authorization: Token <your-token>`

---

## 🚜 FARMER ENDPOINTS

| Method | Endpoint                             | Description               |
|--------|--------------------------------------|---------------------------|
| GET    | `/api/v1/farmer/`                    | List all farmers          |
| POST   | `/api/v1/farmer/`                    | Create new farmer         |
| GET    | `/api/v1/farmer/<phone_number>/`     | Retrieve specific farmer  |
| PUT    | `/api/v1/farmer/<phone_number>/`     | Update farmer             |
| DELETE | `/api/v1/farmer/<phone_number>/`     | Delete farmer             |

- `produce` is a nested field in responses

---

## 🍅 PRODUCE (nested)

- Managed through `Farmer` serializer
- No standalone endpoint yet
- Linked 1:N from Farmer

---

## 🧍‍♂️ BUYER ENDPOINTS

| Method | Endpoint                             | Description               |
|--------|--------------------------------------|---------------------------|
| GET    | `/api/v1/buyer/`                     | List all buyers           |
| POST   | `/api/v1/buyer/`                     | Create buyer (signup)     |
| GET    | `/api/v1/buyer/<phone_number>/`      | Get buyer with cart/orders|
| PUT    | `/api/v1/buyer/<phone_number>/`      | Update buyer              |
| DELETE | `/api/v1/buyer/<phone_number>/`      | Delete buyer              |

- Includes nested: `cart`, `orders`

---

## 🛒 CART MANAGEMENT

| Method  | Endpoint                   | Description             |
|---------|----------------------------|-------------------------|
| POST    | `/api/v1/cart/`            | Add item to cart        |
| PUT     | `/api/v1/cart/<id>/`       | Update cart item qty    |
| PATCH   | `/api/v1/cart/<id>/`       | Update cart item qty    |
| DELETE  | `/api/v1/cart/<id>/`       | Remove cart item        |

### Example Payload for Add:
```json
{
  "produce": 1,
  "quantity": 3
}
```

---

## 📦 ORDER MANAGEMENT

| Method | Endpoint                              | Description                       |
|--------|---------------------------------------|-----------------------------------|
| POST   | `/api/v1/orders/create-from-cart/`    | Create new "PENDING" order        |
| POST   | `/api/v1/orders/<id>/confirm/`        | Confirm payment for order         |

### Order Status Options:
- `PENDING`: Waiting for payment
- `CONFIRMED`: Paid
- `CANCELLED`: (future)

---

## 🚦 ORDER LIFECYCLE

1. Add items to cart
2. Call `/orders/create-from-cart/` → creates a `PENDING` order
3. Call `/orders/<id>/confirm/` → confirms payment
4. Order marked as `CONFIRMED`

---

## 🔒 SECURITY

- All endpoints require `TokenAuthentication`
- Buyer & Farmer models are linked to Django `User`
- Only authenticated users can access their resources

---

## ✅ FUTURE ENHANCEMENTS

- Webhook-based payment confirmation
- Separate produce CRUD API
- Cancel / expire unpaid orders
- Add payment metadata to orders
- Role-based permissions

