import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to Task Management System!</h1>
      <p>Your simple solution for managing daily tasks.</p>
      {isAuthenticated ? (
        <Link to="/dashboard">
          <button>Go to your Dashboard</button>
        </Link>
      ) : (
        <Link to="/login">
          <button>Login to get started</button>
        </Link>
      )}
    </div>
  );
};

export default HomePage;