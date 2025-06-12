import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="navbar-brand">
          🌾 AgriKart
        </Link>
      </div>

      <div className="navbar-right">
        <Link to="/">
          <i className="fas fa-home"></i> Home
        </Link>

        {user?.is_farmer && (
          <Link to="/dashboard/farmer">
            <i className="fas fa-tractor"></i> Dashboard
          </Link>
        )}

        {user && !user?.is_farmer && (
          <Link to="/cart">
            <i className="fas fa-shopping-cart"></i> Cart
          </Link>
        )}

        {user ? (
          <button className="btn-logout" onClick={logout}>
            <i className="fas fa-sign-out-alt"></i> Logout
          </button>
        ) : (
          <Link to="/login">
            <i className="fas fa-sign-in-alt"></i> Login
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
