import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

import '../styles/Dashboard.css';

const FarmerDashboard = () => {
  const { user } = useAuth();
  const [produceList, setProduceList] = useState([]);
  const [farmerInfo, setFarmerInfo] = useState(null);
  const [form, setForm] = useState({ name: '', price: '', quantity: '', category: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    if (!user) return;
    fetchDashboard();
  }, [user]);

  const fetchDashboard = async () => {
    try {
      const res = await api.get(`/api/v1/farmer/${user.phone}/`);
      setFarmerInfo({
        name: res.data.name,
        address: res.data.address,
        phone: user.phone,
        joined: res.data.joined || 'N/A',
      });
      setProduceList(res.data.produce || []);
    } catch (err) {
      alert('Failed to fetch dashboard data');
    }
  };

  const categoryData = () => {
    const counts = {};
    produceList.forEach(item => {
      const cat = item.category?.trim() || 'Uncategorized';
      counts[cat] = (counts[cat] || 0) + 1;
    });

    const labels = Object.keys(counts);
    const data = Object.values(counts);

    return {
      labels,
      datasets: [{
        data,
        backgroundColor: [
          '#66bb6a', '#ffa726', '#42a5f5', '#ab47bc', '#ff7043', '#26c6da'
        ],
        borderWidth: 1
      }],
      plugins: {
        datalabels: {
          color: '#fff',
          font: {
            weight: 'bold',
            size: 14,
            family: 'Nunito, Segoe UI, sans-serif',
          },
          textShadowColor: 'rgba(0, 0, 0, 0.25)',
          textShadowBlur: 4,
          formatter: (value, ctx) => {
            const total = ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            const label = ctx.chart.data.labels[ctx.dataIndex];
            return `${label}\n${percentage}%`;
          },
          align: 'center',
          anchor: 'center',
          clamp: true,
          borderRadius: 4,
          padding: 6,
        }
      }
    };
  };

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { name, price, quantity, category } = form;
    if (!name || !price || !quantity || !category) return alert("Fill all fields.");

    try {
      if (editingId) {
        await api.put(`/api/v1/produce/${editingId}/`, form);
      } else {
        await api.post('/api/v1/produce/', form);
      }
      setForm({ name: '', price: '', quantity: '', category: '' });
      setEditingId(null);
      fetchDashboard();
    } catch (err) {
      alert('Error saving produce.');
    }
  };

  const handleEdit = (item) => {
    setForm({
      name: item.name,
      price: item.price,
      quantity: item.quantity,
      category: item.category || ''
    });
    setEditingId(item.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this produce item?")) return;
    try {
      await api.delete(`/api/v1/produce/${id}/`);
      fetchDashboard();
    } catch {
      alert("Delete failed.");
    }
  };

  const totalQty = produceList.reduce((acc, item) => acc + parseInt(item.quantity || 0), 0);

  return (
    <div className="farmer-dashboard-grid">
      {/* Sidebar Info Card */}
      <aside className="sidebar-card">
        <h3>Farmer Profile</h3>
        {farmerInfo ? (
          <ul>
            <li><strong>Name:</strong> {farmerInfo.name}</li>
            <li><strong>Phone:</strong> {farmerInfo.phone}</li>
            <li><strong>Address:</strong> {farmerInfo.address}</li>
          </ul>
        ) : <p>Loading info...</p>}

        {produceList.length > 0 && (
          <div className="category-chart">
            <h4>Product by Category</h4>
            <Pie data={categoryData()} options={{ plugins: { datalabels: {} } }} />
          </div>
        )}
      </aside>

      {/* Main Dashboard */}
      <div className="main-panel">
        <h2>Dashboard</h2>

        <div className="stats-grid">
          <div className="stat-card">
            <h4>Total Items</h4>
            <p>{produceList.length}</p>
          </div>
          <div className="stat-card">
            <h4>Total Quantity</h4>
            <p>{totalQty}</p>
          </div>
        </div>

        {/* Add/Edit Produce Form */}
        <div className="produce-form">
          <h3>{editingId ? 'Edit Produce' : 'Add New Product'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="field-group">
              <label htmlFor="name">Product Name</label>
              <input
                id="name"
                name="name"
                placeholder="E.g. Tomatoes"
                value={form.name}
                onChange={handleChange}
              />
            </div>

            <div className="field-group">
              <label htmlFor="category">Category</label>
              <select
                id="category"
                name="category"
                value={form.category}
                onChange={handleChange}
              >
                <option value="">Select category</option>
                <option value="Fruits">Fruits</option>
                <option value="Vegetables">Vegetables</option>
                <option value="Dairy">Dairy</option>
                <option value="Grains">Grains</option>
                <option value="Organic">Organic</option>
              </select>
            </div>

            <div className="field-group">
              <label htmlFor="price">Price (₹)</label>
              <input
                id="price"
                name="price"
                type="number"
                placeholder="E.g. 50"
                value={form.price}
                onChange={handleChange}
              />
            </div>

            <div className="field-group">
              <label htmlFor="quantity">Quantity</label>
              <input
                id="quantity"
                name="quantity"
                type="number"
                placeholder="E.g. 100"
                value={form.quantity}
                onChange={handleChange}
              />
            </div>

            <button type="submit">
              {editingId ? 'Update Produce' : 'Add Produce'}
            </button>
          </form>
        </div>

        {/* Produce List */}
        <div className="card produce-list">
          <h3>My Products</h3>
          {produceList.length === 0 ? (
            <p>No product listed.</p>
          ) : (
            <ul>
              {produceList.map(item => (
                <li key={item.id}>
                  <span>
                    {item.name} - ₹{item.price} - Qty: {item.quantity} - <em>{item.category || 'Uncategorized'}</em>
                  </span>
                  <div className="btn-group">
                    <button className="edit" onClick={() => handleEdit(item)}>Edit</button>
                    <button className="delete" onClick={() => handleDelete(item.id)}>Delete</button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default FarmerDashboard;
