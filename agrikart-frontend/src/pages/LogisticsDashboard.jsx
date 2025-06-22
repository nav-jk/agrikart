import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/api';
import '../styles/LogisticsDashboard.css';

const LogisticsDashboard = () => {
  const [orders, setOrders] = useState([]);
  const token = localStorage.getItem('access');
  const [statusUpdateMap, setStatusUpdateMap] = useState({});

  useEffect(() => {
    if (!token) return;

    api
      .get('/api/v1/logistics/orders/nearby/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => setOrders(res.data))
      .catch((err) => console.error('Error fetching nearby orders:', err));
  }, [token]);

  const handleStatusChange = (orderId, newStatus) => {
    setStatusUpdateMap((prev) => ({
      ...prev,
      [orderId]: newStatus,
    }));
  };

  const updateStatus = async (orderId) => {
    const newStatus = statusUpdateMap[orderId];
    if (!newStatus) return alert('Please select a status.');

    try {
      await api.patch(
        `/api/v1/logistics/orders/${orderId}/status/`,
        { status: newStatus },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setOrders((prev) =>
        prev.map((order) =>
          order.order_id === orderId
            ? { ...order, status: newStatus }
            : order
        )
      );

      alert('Status updated successfully!');
    } catch (err) {
      console.error('Status update failed:', err);
      alert('Failed to update order status.');
    }
  };

  const downloadReceipt = async (orderId) => {
    try {
      const res = await api.get(`/api/v1/logistics/orders/${orderId}/receipt/`, {
        responseType: 'blob',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `order-${orderId}-receipt.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Receipt download failed:', err);
      alert('Failed to download receipt.');
    }
  };

  const getStatusSummary = () => {
    const summary = {
      confirmed: 0,
      pending: 0,
      in_transit: 0,
      delivered: 0,
    };

    orders.forEach((order) => {
      const status = order.status?.toLowerCase();
      if (summary[status] !== undefined) {
        summary[status]++;
      }
    });

    return summary;
  };

  const summary = getStatusSummary();

  return (
    <div className="logistics-dashboard">
      <h2 className="dashboard-title">Nearby Pickup Orders</h2>

      <div className="summary-pill-row">
        <div className="summary-pill blue">
          <span className="count">{orders.length}</span>
          <span>Total Orders</span>
        </div>
        <div className="summary-pill green">
          <span className="count">{summary.confirmed}</span>
          <span>Confirmed</span>
        </div>
        <div className="summary-pill yellow">
          <span className="count">{summary.pending}</span>
          <span>Pending</span>
        </div>
        <div className="summary-pill purple">
          <span className="count">{summary.delivered}</span>
          <span>Delivered</span>
        </div>
      </div>

      {orders.length === 0 ? (
        <p className="empty-text">No nearby orders.</p>
      ) : (
        <div className="order-table-container">
          <table className="order-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Status</th>
                <th>Farmer</th>
                <th>Farmer Address</th>
                <th>Buyer Address</th>
                <th>Distance (km)</th>
                <th>Items</th>
                <th>Map</th>
                <th>Update</th>
                <th>Receipt</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.order_id}>
                  <td>#{order.order_id}</td>
                  <td>
                    <span className={`badge ${order.status.toLowerCase()}`}>
                      {order.status.toUpperCase()}
                    </span>
                  </td>
                  <td>{order.farmer_name}</td>
                  <td>{order.farmer_address}</td>
                  <td>{order.buyer_address}</td>
                  <td>{order.distance_km.toFixed(2)}</td>
                  <td>
                    <ul className="item-list">
                      {order.items.map((item, idx) => (
                        <li key={idx}>
                          <span className="item-name">{item.produce.name}</span>
                          <span className="item-qty">× {item.quantity}</span>
                        </li>
                      ))}
                    </ul>
                  </td>
                  <td>
                    <Link
                      to={`/logistics/map?lat=${encodeURIComponent(order.farmer_lat)}&lon=${encodeURIComponent(order.farmer_lon)}&name=${encodeURIComponent(order.farmer_name)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="map-link"
                    >
                      View
                    </Link>
                  </td>
                  <td>
                    <select
                      className="amazon-select"
                      value={statusUpdateMap[order.order_id] || order.status}
                      onChange={(e) => handleStatusChange(order.order_id, e.target.value)}
                    >
                      <option value="CONFIRMED">Confirmed</option>
                      <option value="PICKED_UP">Picked Up</option>
                      <option value="IN_TRANSIT">In Transit</option>
                      <option value="DELIVERED">Delivered</option>
                    </select>
                    <button
                      className="amazon-update-btn"
                      onClick={() => updateStatus(order.order_id)}
                    >
                      Update
                    </button>
                  </td>
                  <td>
                    <button
                      onClick={() => downloadReceipt(order.order_id)}
                      className="receipt-link"
                    >
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default LogisticsDashboard;
