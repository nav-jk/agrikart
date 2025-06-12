import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/api';
import '../styles/payment.css';

const Payment = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const orderId = new URLSearchParams(location.search).get('order_id');
  const [loading, setLoading] = useState(false);

  const confirmPayment = async () => {
    setLoading(true);
    try {
      await api.post(`/api/v1/orders/${orderId}/confirm/`);
      navigate('/', { state: { message: 'Payment successful!' } });
    } catch {
      alert('Payment failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="payment-container">
      <div className="payment-box">
        <h2>Confirm Your Payment</h2>
        <p className="order-info">Order ID: <strong>{orderId}</strong></p>
        <p className="order-note">You're about to complete your purchase. Please confirm your payment to finalize the order.</p>
        <button className="payment-btn" onClick={confirmPayment} disabled={loading}>
          {loading ? 'Processing...' : 'Confirm Payment'}
        </button>
      </div>
    </div>
  );
};

export default Payment;
