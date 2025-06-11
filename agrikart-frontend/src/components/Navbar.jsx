import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navbar.css';


const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav>
      <Link to="/">Home</Link>
      {user?.is_farmer && <Link to="/dashboard/farmer">Dashboard</Link>}
      {!user?.is_farmer && <Link to="/cart">Cart</Link>}
      {user ? (
        <button onClick={logout}>Logout</button>
      ) : (
        <>
          <Link to="/login">Login</Link>
          <Link to="/signup/buyer">Buyer Signup</Link>
          <Link to="/signup/farmer">Farmer Signup</Link>
        </>
      )}
    </nav>
  );
};

export default Navbar;
