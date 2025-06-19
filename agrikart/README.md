# AGRIKART BACKEND API DOCUMENTATION

## TECH STACK

- Django 5
- Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- Swagger Docs (drf-yasg)
- Modular apps: api, buyer, farmer

---

## BASE API URL

```
http://localhost:8000/api/v1/
```

---

## AUTHENTICATION

AgriKart uses JWT (Bearer Token) for secure access.

### Buyer Signup

POST `/auth/signup/`

```json
{
  "username": "buyer1",
  "email": "email@example.com",
  "password": "pass123",
  "phone_number": "9876543210",
  "address": "Buyer Address"
}
```

---

### Farmer Signup

POST `/auth/signup/farmer/`

```json
{
  "username": "farmer1",
  "email": "farmer@example.com",
  "password": "pass123",
  "phone_number": "9876543210",
  "name": "Farmer Name",
  "address": "Farm Address"
}
```

---

### Login (All Users)

POST `/auth/token/`

```json
{
  "username": "user1",
  "password": "pass123"
}
```

Returns:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Use in headers:

```
Authorization: Bearer <access-token>
```

Tokens include:
- username
- email
- is_farmer
- is_buyer
- phone_number

---

## FARMER API

### List/Create Farmer

GET/POST `/farmer/`

### Retrieve/Update/Delete by Phone

GET/PUT/DELETE `/farmer/<phone_number>/`

Example response:

```json
{
  "id": 1,
  "name": "Farmer Joe",
  "address": "123 Farmville",
  "produce": [
    {
      "id": 1,
      "name": "Tomatoes",
      "price": 20.5,
      "quantity": 100
    }
  ]
}
```

---

## PRODUCE (Nested)

- Produce is returned inside the Farmer response
- No standalone endpoint

---

## BUYER API

### List/Create Buyer

GET/POST `/buyer/`

### Get/Update/Delete by Phone

GET/PUT/DELETE `/buyer/<phone_number>/`

Includes:
- cart (nested cart items)
- orders (order IDs)

---

## CART MANAGEMENT

| Method  | Endpoint         | Description             |
|---------|------------------|-------------------------|
| POST    | `/cart/`         | Add item to cart        |
| PUT     | `/cart/<id>/`    | Update item quantity    |
| PATCH   | `/cart/<id>/`    | Update item quantity    |
| DELETE  | `/cart/<id>/`    | Remove item from cart   |

Add item payload:

```json
{
  "produce": 1,
  "quantity": 3
}
```

---

## ORDER MANAGEMENT

### Create Order from Cart

POST `/orders/create-from-cart/`

- Converts all cart items into a PENDING order
- Clears the cart

---

### Confirm Order

POST `/orders/<id>/confirm/`

- Marks order as CONFIRMED (simulated payment)

---

### ORDER STATUS

- PENDING: Created, waiting for payment
- CONFIRMED: Payment successful
- CANCELLED: (Planned for future)

---

## FRONTEND DEVELOPER GUIDE

### Home Page (All Users)

- Display all produce from all farmers
- Show: name, price, quantity, farmer name
- Include "Add to Cart" button

On Add to Cart:
- Call POST /cart/
- Requires buyer to be logged in

---

### Buyer Authentication

- Sign up: POST /auth/signup/
- Login: POST /auth/token/
- Store access token in localStorage or cookies
- Use token in headers:

```
Authorization: Bearer <access-token>
```

---

### Buyer Home = Dashboard

- After login, redirect to home
- Buyer sees:
  - Available products
  - Option to go to cart
  - Option to place order

---

### Cart Page

- List items from buyer’s cart (via /buyer/<phone_number>/)
- Allow:
  - Quantity update (PUT/PATCH)
  - Remove item (DELETE)
- Show total and place order button

---

### Dummy Payment Page

After calling `/orders/create-from-cart/`, redirect to:

```
/payment?order_id=<id>
```

- Show order summary
- On confirm, call: `/orders/<id>/confirm/`
- Show success message and return to home

---

### Farmer Dashboard

- After farmer login:
  - Call `/farmer/<phone_number>/`
- Display:
  - Name
  - Address
  - List of produce (name, price, quantity)

---

## DEVELOPMENT UTILITIES

| Feature      | URL            |
|--------------|----------------|
| Admin Panel  | `/admin/`      |
| Swagger Docs | `/swagger/`    |
| ReDoc        | `/redoc/`      |

---

## SECURITY AND ACCESS

- All API calls are JWT protected
- Buyers and farmers are isolated
- Roles are embedded in JWT token
- Swagger available for testing

---

## FUTURE ROADMAP

- Add image uploads for produce
- Add buyer order history page
- Add farmer produce management UI
- Integrate real payment gateway
- Implement order cancellation flow
#  WhatsApp Integration

The WhatsApp integration for this project is being handled by [@debdip4](https://github.com/debdip4).

## 🔗 GitHub Repository

You can find the integration logic and updates here:  
[https://github.com/annam-ai-iitropar/team_2A/tree/main/AgriKart_Whatsapp_Bot](https://github.com/annam-ai-iitropar/team_2A/tree/main/AgriKart_Whatsapp_Bot)

##  Status

- [x] Integration in progress  
- [ ] Final testing  
- [ ] Deployment
