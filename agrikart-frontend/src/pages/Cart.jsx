import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';
import { useNavigate } from 'react-router-dom';

const Cart = () => {
  const [cart, setCart] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return;
    api.get(`/api/v1/buyer/${user.phone}/`)
      .then(res => setCart(res.data.cart))
      .catch(() => alert('Error loading cart'));
  }, [user]);

  const updateQuantity = async (id, quantity) => {
    await api.patch(`/api/v1/cart/${id}/`, { quantity });
    setCart(prev => prev.map(item => item.id === id ? { ...item, quantity } : item));
  };

  const removeItem = async (id) => {
    await api.delete(`/api/v1/cart/${id}/`);
    setCart(prev => prev.filter(item => item.id !== id));
  };

  const placeOrder = async () => {
    if (!cart.length) return alert("Cart is empty");
    const res = await api.post('/api/v1/orders/create-from-cart/');
    navigate(`/payment?order_id=${res.data.id}`);
  };

  return (
    <div>
      <h2>My Cart</h2>
      {cart.length === 0 ? <p>No items in cart.</p> : (
        cart.map(item => (
          <div key={item.id}>
            <p>{item.produce.name} - ₹{item.produce.price} x {item.quantity}</p>
            <input
              type="number"
              min="1"
              value={item.quantity}
              onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
            />
            <button onClick={() => removeItem(item.id)}>Remove</button>
          </div>
        ))
      )}
      {cart.length > 0 && <button onClick={placeOrder}>Place Order</button>}
    </div>
  );
};

export default Cart;
