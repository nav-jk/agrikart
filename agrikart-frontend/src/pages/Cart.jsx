import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';
import { useNavigate } from 'react-router-dom';
import '../styles/cart.css';

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
    if (quantity < 1) return;
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
    <div className="cart-container">
      <h2>Shopping Cart</h2>

      {cart.length === 0 ? (
        <p className="empty-message">Your cart is currently empty.</p>
      ) : (
        <div className="cart-list">
          {cart.map(item => (
            <div className="cart-item" key={item.id}>
              <div className="item-info">
                <p className="item-name">{item.produce_info.name}</p>
                <p className="item-price">₹{item.produce_info.price} each</p>
              </div>
              <div className="item-actions">
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                  className="qty-input"
                />
                <p className="item-total">Subtotal: ₹{item.produce_info.price * item.quantity}</p>
                <button className="remove-btn" onClick={() => removeItem(item.id)}>Remove</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {cart.length > 0 && (
        <button className="place-order-btn" onClick={placeOrder}>Proceed to Checkout</button>
      )}
    </div>
  );
};

export default Cart;
