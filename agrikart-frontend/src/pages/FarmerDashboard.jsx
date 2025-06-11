import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';

const FarmerDashboard = () => {
  const { user } = useAuth();
  const [produceList, setProduceList] = useState([]);
  const [farmerInfo, setFarmerInfo] = useState(null);

  useEffect(() => {
    if (!user) return;
    api.get(`/api/v1/farmer/${user.phone}/`).then(res => {
      setFarmerInfo({ name: res.data.name, address: res.data.address });
      setProduceList(res.data.produce || []);
    }).catch(() => alert('Failed to fetch dashboard data'));
  }, [user]);

  return (
    <div>
      <h2>Farmer Dashboard</h2>
      {farmerInfo && (
        <div>
          <p>Name: {farmerInfo.name}</p>
          <p>Address: {farmerInfo.address}</p>
        </div>
      )}
      <h3>My Produce</h3>
      {produceList.length === 0 ? (
        <p>No produce listed.</p>
      ) : (
        produceList.map(item => (
          <div key={item.id}>
            <p>{item.name} - ₹{item.price} - Qty: {item.quantity}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default FarmerDashboard;
