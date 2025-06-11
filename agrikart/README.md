# AgriKart Backend API docs

---

##  TECH STACK

- Django 5
- Django REST Framework
- JWT Authentication (`djangorestframework-simplejwt`)
- Swagger Docs (`drf-yasg`)
- Modular apps: `api`, `buyer`, `farmer`

---

##  BASE API URL

```
http://localhost:8000/api/v1/
```

---

##  AUTHENTICATION

FarmHub uses **JWT (Bearer Token)** for secure access.

###  Buyer Signup

**POST** `/auth/signup/`

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

###  Farmer Signup

**POST** `/auth/signup/farmer/`

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

###  Login (All Users)

**POST** `/auth/token/`

```json
{
  "username": "user1",
  "password": "pass123"
}
```

**Returns:**

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

**Use in headers:**

```
Authorization: Bearer <access-token>
```

---

##  FARMER API

###  List/Create Farmer

**GET/POST** `/farmer/`

###  Retrieve/Update/Delete by Phone

**GET/PUT/DELETE** `/farmer/<phone_number>/`

**Response:**

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

##  PRODUCE (Nested)

- Produce is returned inside the `Farmer` response
- No standalone endpoint (yet)

---

##  BUYER API

###  List/Create Buyer

**GET/POST** `/buyer/`

###  Get/Update/Delete by Phone

**GET/PUT/DELETE** `/buyer/<phone_number>/`

**Includes:**
- `cart` (nested cart items)
- `orders` (order IDs only for now)

---

## 🛒 CART MANAGEMENT

| Method  | Endpoint         | Description             |
|---------|------------------|-------------------------|
| POST    | `/cart/`         | Add item to cart        |
| PUT     | `/cart/<id>/`    | Update item quantity    |
| PATCH   | `/cart/<id>/`    | Update item quantity    |
| DELETE  | `/cart/<id>/`    | Remove item from cart   |

**Add item payload:**

```json
{
  "produce": 1,
  "quantity": 3
}
```

---

##  ORDER MANAGEMENT

###  Create Order from Cart

**POST** `/orders/create-from-cart/`

- Moves cart items to a `PENDING` order
- Empties the cart

---

###  Confirm Order

**POST** `/orders/<id>/confirm/`

- Marks order as `CONFIRMED` (simulated payment)

---

###  ORDER STATUS

- `PENDING`: Created, waiting for payment
- `CONFIRMED`: Payment successful
- `CANCELLED`: (Future)

---

##  FRONTEND DEVELOPER GUIDE

---

###  Home Page

- Show list of all **produce** from all farmers
- Display name, price, quantity, farmer name
- Show "Add to Cart" button for each item

**On Add to Cart:**

- Make `POST /cart/` request
- Requires login as buyer

---

###  Buyer Authentication

- Sign up via `/auth/signup/`
- Login via `/auth/token/`
- Save `access` token in localStorage or cookie
- Send JWT in headers:

```
Authorization: Bearer <access-token>
```

---

###  Buyer Dashboard = Home Page

- After login, redirect to home
- Buyer sees:
  - All produce
  - Cart item count
  - Link to Cart page
  - Option to place order

---

###  Cart Page

- List buyer’s cart items
  - Get from `/buyer/<phone_number>/`
- Buttons to update quantity or remove items
- Button: **Place Order**

---

###  Dummy Payment Page

- After creating order (`/orders/create-from-cart/`)
- Redirect user to:

```
/payment?order_id=<id>
```

- Simulate payment
- On confirmation:
  - POST to `/orders/<id>/confirm/`
  - Show success message
  - Redirect to homepage

---

###  Farmer Dashboard

- After farmer login:
  - Fetch `/farmer/<phone_number>/`
- Show:
  - Farmer name and address
  - List of produce with:
    - Name
    - Price
    - Quantity

---

## 🛠 DEV UTILITIES

| Tool         | URL                 |
|--------------|---------------------|
| Admin Panel  | `/admin/`           |
| Swagger Docs | `/swagger/`         |
| ReDoc        | `/redoc/`           |

---

##  SECURITY & ACCESS

- All routes are JWT protected
- Buyer can only view/edit own cart, orders
- Farmer can only view own produce
- Swagger available without auth (for testing)

---


##  FUTURE IMPROVEMENTS

- Image uploads for produce
- Buyer order history endpoint
- Role-based permissions
- Payment gateway integration
- Farmer produce add/edit/delete UI

---
