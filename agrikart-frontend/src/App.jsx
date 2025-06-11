import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import RequireAuth from './routes/RequireAuth';
import RequireFarmer from './routes/RequireFarmer';
import Login from './pages/Login';
import SignupBuyer from './pages/SignupBuyer';
import SignupFarmer from './pages/SignupFarmer';
import Home from './pages/Home';
import Cart from './pages/Cart';
import Payment from './pages/Payment';
import FarmerDashboard from './pages/FarmerDashboard';
import Navbar from './components/Navbar';

function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup/buyer" element={<SignupBuyer />} />
        <Route path="/signup/farmer" element={<SignupFarmer />} />
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<RequireAuth><Cart /></RequireAuth>} />
        <Route path="/payment" element={<RequireAuth><Payment /></RequireAuth>} />
        <Route path="/dashboard/farmer" element={
          <RequireAuth>
            <RequireFarmer>
              <FarmerDashboard />
            </RequireFarmer>
          </RequireAuth>
        } />
      </Routes>
    </AuthProvider>
  );
}

export default App;
