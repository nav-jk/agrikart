import { useEffect, useState } from 'react';
import api from '../api/api';
import '../styles/Me.css'; // Optional CSS

const Me = () => {
  const [profile, setProfile] = useState(null);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('access');
    if (!token) return;

    api.get('/api/v1/auth/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      setProfile(res.data);
      return api.get('/api/v1/buyer/orders/mine/', {
        headers: { Authorization: `Bearer ${token}` }
      });
    })
    .then(orderRes => {
      setOrders(orderRes.data || []);
    })
    .catch(err => {
      console.error('Error fetching profile or orders:', err);
    });
  }, []);

  if (!profile) return <p>Loading profile...</p>;

  return (
    <div className="profile-container">
      <h2>My Profile</h2>
      <div className="profile-info">
        <p><strong>Name:</strong> {profile.user?.username || profile.user?.name}</p>
        <p><strong>Phone:</strong> {profile.buyer?.user?.phone_number || profile.farmer?.user?.phone_number}</p>
        <p><strong>Address:</strong> {profile.buyer?.address || profile.farmer?.address}</p>
        <p><strong>Role:</strong> {profile.user?.is_farmer ? 'Farmer' : 'Buyer'}</p>
      </div>

      {!profile.user?.is_farmer && (
        <>
          <h3>Order History</h3>
          {orders.length === 0 ? (
            <p>No orders yet.</p>
          ) : (
            <ul className="order-list">
              {orders.map(order => (
                <li key={order.id} className="order-item">
                  <p><strong>Order #{order.id}</strong></p>
                  <p>Status: <span className={`status ${order.status.toLowerCase()}`}>{order.status}</span></p>
                  <p>Date: {new Date(order.created_at).toLocaleString()}</p>

                  <table className="order-table">
                    <thead>
                      <tr>
                        <th>Produce</th>
                        <th>Price</th>
                        <th>Qty</th>
                        <th>Subtotal</th>
                      </tr>
                    </thead>
                    <tbody>
                      {order.items.map((item, index) => {
                        const { produce, quantity } = item;
                        const subtotal = produce.price * quantity;
                        return (
                          <tr key={index}>
                            <td>{produce.name}</td>
                            <td>₹{produce.price}</td>
                            <td>{quantity}</td>
                            <td>₹{subtotal}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>

                  <p className="order-total"><strong>Total:</strong> ₹{order.total}</p>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
};

export default Me;
