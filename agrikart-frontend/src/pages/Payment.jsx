import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/api';

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
    <div>
      <h2>Payment</h2>
      <p>Confirm payment for Order ID: {orderId}</p>
      <button onClick={confirmPayment} disabled={loading}>
        {loading ? 'Processing...' : 'Confirm Payment'}
      </button>
    </div>
  );
};

export default Payment;
