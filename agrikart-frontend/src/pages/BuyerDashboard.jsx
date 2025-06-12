import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';
import '../styles/BuyerDashboard.css';

const BuyerDashboard = () => {
  const [produce, setProduce] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [addedToCart, setAddedToCart] = useState({});
  const [quantityError, setQuantityError] = useState({});
  const [loading, setLoading] = useState(true);

  const { user } = useAuth();
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const categoryFilter = query.get('category');

  useEffect(() => {
    api.get('/api/v1/farmer/')
      .then((res) => {
        setProduce(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to fetch produce', err);
        setLoading(false);
      });
  }, []);

  const handleQuantityChange = (produceId, value) => {
    setQuantities(prev => ({ ...prev, [produceId]: value }));
    setQuantityError(prev => ({ ...prev, [produceId]: false }));
  };

  const handleAddToCart = async (produceId) => {
    const quantity = parseInt(quantities[produceId] || 0);
    if (!quantity || quantity <= 0) {
      setQuantityError(prev => ({ ...prev, [produceId]: true }));
      return;
    }

    try {
      await api.post('/api/v1/cart/', {
        produce: produceId,
        quantity,
      });

      setQuantities(prev => ({ ...prev, [produceId]: '' }));
      setAddedToCart(prev => ({ ...prev, [produceId]: true }));
      setQuantityError(prev => ({ ...prev, [produceId]: false }));

      setTimeout(() => {
        setAddedToCart(prev => ({ ...prev, [produceId]: false }));
      }, 2000);
    } catch (err) {
      console.error('Add to cart error:', err.response?.data || err.message);
      alert('Error adding to cart. Make sure you are logged in as a buyer.');
    }
  };

  return (
    <div className="container">
      <h2>Marketplace {categoryFilter ? ` - ${categoryFilter}` : ''}</h2>
      {loading ? (
        <p>Loading produce...</p>
      ) : produce.length === 0 ? (
        <p>No produce available right now.</p>
      ) : (
        <div className="produce-grid">
          {produce.map((farmer) =>
            farmer.produce
              .filter(item =>
                !categoryFilter || item.category?.toLowerCase() === categoryFilter.toLowerCase()
              )
              .map((item) => (
                <div className="produce-card" key={item.id}>
                  <h3>{item.name}</h3>
                  <p>₹{item.price} &middot; Stock: {item.quantity}</p>
                  <p><strong>Farmer:</strong> {farmer.name}</p>

                  <div className="quantity-cart">
                    <select
                      className={`qty-select ${quantityError[item.id] ? 'error' : ''}`}
                      value={quantities[item.id] || ''}
                      onChange={(e) => handleQuantityChange(item.id, e.target.value)}
                    >
                      <option value="">Qty</option>
                      {[...Array(Math.min(10, item.quantity)).keys()].map((i) => (
                        <option key={i + 1} value={i + 1}>
                          {i + 1}
                        </option>
                      ))}
                    </select>
                    <button
                      className={`add-cart-btn ${addedToCart[item.id] ? 'added' : ''}`}
                      onClick={() => handleAddToCart(item.id)}
                      disabled={addedToCart[item.id]}
                    >
                      {addedToCart[item.id] ? 'Added ✅' : 'Add to Cart'}
                    </button>
                  </div>

                  {quantityError[item.id] && (
                    <p className="qty-error-text">Please select a quantity.</p>
                  )}
                </div>
              ))
          )}
        </div>
      )}
    </div>
  );
};

export default BuyerDashboard;
