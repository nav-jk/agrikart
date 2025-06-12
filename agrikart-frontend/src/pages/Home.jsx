import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      if (user.is_farmer) {
        navigate('/dashboard/farmer');
      } else {
        navigate('/dashboard/buyer');
      }
    }
  }, [user, navigate]);

  return (
    <div className="home-page">
      {/* Combined Hero + Auth Box */}
      <div className="hero-section">
        <div className="hero-text">
          <h1>Freshness Delivered 🍅🥦</h1>
          <p>Shop directly from India's best local farms — no middlemen, just better food.</p>
          <p className="subline">Welcome to <strong>AgriKart</strong> — your personalized agri-commerce platform.</p>

          <div className="auth-buttons">
            <Link className="btn" to="/signup/buyer">Sign Up as Buyer</Link>
            <span style={{ margin: '0 10px', color: '#888' }}>|</span>
            <Link className="btn" to="/signup/farmer">Sign Up as Farmer</Link>
            <span style={{ margin: '0 10px', color: '#888' }}>|</span>
            <Link className="btn-outline" to="/login">Login</Link>
          </div>
        </div>
        <div className="hero-image">
          <img src="/hero-veg.jpg" alt="AgriKart Hero" />
        </div>
      </div>

      {/* Category Cards */}
      <div className="category-section">
        <h2>Shop by Category</h2>
        <div className="category-grid">
          {[
            { label: 'Fruits', img: '/fruits.jpg' },
            { label: 'Vegetables', img: '/vegetables.jpg' },
            { label: 'Organic', img: '/organic.jpg' },
            { label: 'Dairy', img: '/dairy.jpg' },
            { label: 'Grains', img: '/grains.jpg' },
          ].map((cat, index) => (
            <div
              className="category-card"
              key={index}
              onClick={() => navigate(`/login?redirect=/dashboard/buyer&category=${cat.label}`)}
              style={{ cursor: 'pointer' }}
            >
              <img src={cat.img} alt={cat.label} />
              <p>{cat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
