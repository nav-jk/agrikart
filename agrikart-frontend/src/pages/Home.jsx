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

  return (
    <div className="container">
      <header className="welcome-section">
        <h1>Welcome to AgriKart 🌾</h1>
        <p className="welcome-text">
          Fresh produce straight from local farms to your doorstep. Support farmers, eat healthy, and shop responsibly.
        </p>

        {user ? (
          user.is_farmer && (
            <div className="auth-link">
              <Link to="/dashboard/farmer">Go to Farmer Dashboard</Link>
            </div>
          )
        ) : (
          <div className="auth-prompt">
            <p>New here?</p>
            <Link className="btn" to="/signup/buyer">Sign Up as Buyer</Link>
            <Link className="btn" to="/signup/farmer">Sign Up as Farmer</Link>
            <span style={{ margin: '0 10px', color: '#888' }}>|</span>
            <Link className="btn-outline" to="/login">Login</Link>
          </div>
        )}
      </header>
    </div>
  );
};

export default Home;
