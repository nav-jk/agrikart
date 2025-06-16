# 📘 AgriKart Frontend – Developer Documentation

## ✅ Purpose
This document outlines the structure, features, and workflows of the **AgriKart frontend**, built with React. It includes page descriptions, API integration, role-based routing, and authentication flow.

---

## 🛠️ Tech Stack

| Area        | Technology              |
|-------------|--------------------------|
| Framework   | React (Vite)             |
| Routing     | react-router-dom         |
| Auth        | JWT + localStorage       |
| State Mgmt  | React Context API        |
| Styling     | Custom CSS               |
| HTTP Client | Axios                    |

---

## 🔐 Authentication & Routing

- **Login Endpoint**: `POST /api/v1/auth/token/`
- **Token Handling**: Saved in `localStorage` → decoded to get user info
- **Redirect Logic**:
  - `is_farmer` → `/dashboard/farmer`
  - `is_buyer` → `/dashboard/buyer`
- **Axios Auth Header**:


### 🛡️ Route Guards

```jsx
<Route path="/dashboard/farmer" element={
<RequireAuth>
  <RequireFarmer>
    <FarmerDashboard />
  </RequireFarmer>
</RequireAuth>
} />

## 🧭 Navigation Pages

### 🏠 Home (`Home.jsx`)
- Hero + category cards  
- Shows signup/login options  
- Auto-redirects if logged in  

---

### 🔐 Login (`Login.jsx`)
- Accepts `?redirect` and `?category` query  
- Redirects based on role after login  

---

### 👥 Signup (`SignupBuyer.jsx`, `SignupFarmer.jsx`)
Sends POST requests to:
- `/api/v1/auth/signup/`  
- `/api/v1/auth/signup/farmer/`  

---

### 📦 Buyer Dashboard (`BuyerDashboard.jsx`)
- Lists all produce (grouped by farmer)  
- Add to cart with quantity input  
- Filters by category via query string  

---

### 🌱 Farmer Dashboard (`FarmerDashboard.jsx`)
- Shows personal info + produce list  
- Add/edit/delete produce  
- Backend sync:
  - `POST /api/v1/produce/`  
  - `PUT /api/v1/produce/:id/`  
  - `DELETE /api/v1/produce/:id/`  

---

### 🛒 Cart (`Cart.jsx`)
- Displays buyer’s cart items  
- Allows:
  - Update quantity (`PATCH`)  
  - Delete item (`DELETE`)  
  - Place order: `POST /orders/create-from-cart/`  

---

### 💳 Payment (`Payment.jsx`)
- Reads `order_id` from query string  
- Confirms payment via: `POST /orders/:id/confirm/`  
- On success → redirects to home  

---

### 👤 Me (`Me.jsx`)
- Fetches: `GET /api/v1/auth/me/`  
- Displays:
  - Name  
  - Phone  
  - Address  
  - Role  

---

## 🔌 Key API Endpoints

| Purpose          | Method | Endpoint                                 |
|------------------|--------|-------------------------------------------|
| Login            | POST   | `/api/v1/auth/token/`                    |
| Get User         | GET    | `/api/v1/auth/me/`                       |
| Buyer Signup     | POST   | `/api/v1/auth/signup/`                   |
| Farmer Signup    | POST   | `/api/v1/auth/signup/farmer/`           |
| Add to Cart      | POST   | `/api/v1/cart/`                          |
| Get Buyer Cart   | GET    | `/api/v1/buyer/<phone>/`                |
| Update Cart Item | PATCH  | `/api/v1/cart/<id>/`                     |
| Delete Cart Item | DELETE | `/api/v1/cart/<id>/`                     |
| Place Order      | POST   | `/api/v1/orders/create-from-cart/`      |
| Confirm Payment  | POST   | `/api/v1/orders/<id>/confirm/`          |
| Buyer Orders     | GET    | `/api/v1/buyer/orders/mine/` ✅ Used Before |

---

## 🔎 AuthContext API

Manages global auth state

### Exposes:
- `user` (decoded from JWT)  
- `login(token)`  
- `logout()`  

### Hook Usage

```jsx
const { user, login, logout } = useAuth();
```jsx

## 🚀 Dev Setup

```bash
npm install
npm run dev
