import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Layout = ({ children }) => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div>
      <header className="header">
        <h1>Task Management</h1>
        <nav>
          <ul>
            {isAuthenticated && (
              <>
                <li><button onClick={handleLogout}>Logout</button></li>
              </>
            )}
          </ul>
        </nav>
      </header>
      <main className="container">
        {children}
      </main>
    </div>
  );
};

export default Layout;