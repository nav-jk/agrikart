import { useEffect, useState } from 'react';
import api from '../api/api';
import '../styles/Me.css'; // Optional: your custom styles

const Me = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access');
    if (!token) return;

    api
      .get('/api/v1/auth/me/', {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setProfile(res.data))
      .catch((err) => console.error('Failed to load profile:', err));
  }, []);

  const downloadReceipt = async (orderId) => {
    const token = localStorage.getItem('access');
    if (!token) return alert("Login required");

    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/auth/orders/${orderId}/receipt/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) throw new Error("Download failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.download = `AgriKart_Receipt_Order_${orderId}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Error downloading receipt:", err);
      alert("Failed to download receipt.");
    }
  };

  if (!profile) return <p>Loading profile...</p>;

  const { user, buyer } = profile;
  const orders = buyer?.orders || [];

  return (
    <div className="me-dashboard">
      {/* Sidebar */}
      <aside className="me-sidebar">
        <div className="sidebar-header">
          <h3>My Account</h3>
        </div>
        <ul className="sidebar-links">
          <li className="active">Orders</li>
          <li>Favorites</li>
          <li>Payments</li>
          <li>Addresses</li>
        </ul>
      </aside>

      {/* Main content */}
      <main className="me-content">
        {/* Top Banner */}
        <div className="profile-banner">
          <div className="profile-details">
            <h2>{user.username}</h2>
            <p>{user.phone_number} &nbsp;•&nbsp; {user.email || 'N/A'}</p>
          </div>
          <button className="edit-btn">Edit Profile</button>
        </div>

        {/* Orders Section */}
        <div className="orders-section">
          <h3>Active Orders</h3>

          {orders.length === 0 ? (
            <p className="no-orders">You haven’t placed any orders yet.</p>
          ) : (
            <div className="order-cards">
              {orders.map((order) => (
                <div key={order.id} className="order-card">
                  <div className="order-card-header">
                    <div>
                      <h4>Order #{order.id}</h4>
                      <p>
                        Status:{' '}
                        <span className={`status ${order.status?.toLowerCase()}`}>
                          {order.status}
                        </span>
                      </p>
                      <p className="order-date">
                        {new Date(order.created_at).toLocaleString()}
                      </p>
                    </div>
                    <div>
                      {order.receipt_pdf_url && (
                        <button
                          className="receipt-btn"
                          onClick={() => downloadReceipt(order.id)}
                        >
                          📄 Download Receipt
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="order-card-body">
                    <p><strong>Address:</strong> {buyer?.address || 'N/A'}</p>
                    <div className="order-actions">
                      <button className="track-btn">Track</button>
                      <button className="help-btn">Help</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Me;
