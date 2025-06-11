import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';

const SignupFarmer = () => {
  const [form, setForm] = useState({ username: '', email: '', phone: '', password: '', name: '', address: '' });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/api/v1/auth/signup/farmer/', form);
    navigate('/login');
  };

  return (
    <form onSubmit={handleSubmit}>
      {['username', 'email', 'phone_number', 'password', 'name', 'address'].map((field) => (
        <input key={field} name={field} onChange={handleChange} placeholder={field} required />
      ))}
      <button type="submit">Sign Up as Farmer</button>
    </form>
  );
};

export default SignupFarmer;
