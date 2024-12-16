import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const AdminDashboard = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    const userToken = localStorage.getItem('tokens');
    const userInfo = localStorage.getItem('userInfo');

    if (pathname !== "/admin" || !userToken || !userInfo) {
      window.location.href = "/";
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>AdminDashboard</div>
  );
};

export default AdminDashboard;