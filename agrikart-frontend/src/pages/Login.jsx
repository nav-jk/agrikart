import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';
import '../styles/Login.css';

const Login = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const query = new URLSearchParams(location.search);
  const redirect = query.get('redirect') || '/';
  const category = query.get('category');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/api/v1/auth/token/', form);
      login(res.data.access);

      const user = JSON.parse(atob(res.data.access.split('.')[1]));
      console.log('Decoded login user:', user);

      if (!user.is_farmer && !user.is_buyer) {
        navigate('/logistics/dashboard');
      } else if (user.is_farmer) {
        navigate('/dashboard/farmer');
      } else {
        const target = category
          ? `${redirect}?category=${encodeURIComponent(category)}`
          : redirect;
        navigate(target);
      }

      console.log('Decoded login user:', user);

    } catch (err) {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="page-wrapper">
      <div className="login-wrapper">
        <form onSubmit={handleSubmit}>
          <h2 className="login-title">Sign in to AgriKart</h2>

          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="Enter your username"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
          />

          <button type="submit">Sign In</button>

          <p className="login-footer">
            New to AgriKart? <a href="/signup/buyer">Create an account</a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
