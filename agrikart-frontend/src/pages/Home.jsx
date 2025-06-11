import { useEffect, useState } from 'react';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  const [produce, setProduce] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    api.get('/api/v1/farmer/').then((res) => setProduce(res.data));
  }, []);

  const addToCart = async (itemId) => {
    try {
      await api.post('/api/v1/cart/', { produce_id: itemId });
    } catch {
      alert('Login required');
    }
  };

  return (
    <div>
      {user?.is_farmer && <Link to="/dashboard/farmer">Go to Farmer Dashboard</Link>}
      {produce.map((farmer) =>
        farmer.produce.map((item) => (
          <div key={item.id}>
            <p>{item.name} - ₹{item.price} - Qty: {item.quantity}</p>
            <button onClick={() => addToCart(item.id)}>Add to Cart</button>
          </div>
        ))
      )}
    </div>
  );
};

export default Home;
