import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';
import '../styles/SignupBuyer.css';

const SignupBuyer = () => {
  const [form, setForm] = useState({ username: '', email: '', phone: '', password: '', address: '' });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/api/v1/auth/signup/', form);
    navigate('/login');
  };

  return (
    <form onSubmit={handleSubmit}>
      {['username', 'email', 'phone_number', 'password', 'address'].map((field) => (
        <input key={field} name={field} type={field === 'password' ? 'password' : 'text'} onChange={handleChange} placeholder={field} required />
      ))}
      <button type="submit">Sign Up as Buyer</button>
    </form>
  );
};

export default SignupBuyer;
