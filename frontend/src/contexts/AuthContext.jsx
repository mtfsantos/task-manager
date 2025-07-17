import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check for token on initial load
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      // In a real app, you'd validate the token with the backend
      // For this mock, we just assume presence means authenticated
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await api.post('/login', new URLSearchParams({
        username: username,
        password: password,
      }), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      const { access_token } = response.data;
      localStorage.setItem('authToken', access_token);
      setIsAuthenticated(true);
      // Set the default Authorization header for future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    } catch (error) {
      throw error; // Re-throw to be caught by the Login component
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    delete api.defaults.headers.common['Authorization'];
  };

  // If there's a token on load, set it in the Axios defaults
  // This needs to run *after* the initial useEffect for authentication status
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, [isAuthenticated]); // Rerun if isAuthenticated changes (e.g., after login/logout)


  const value = {
    isAuthenticated,
    login,
    logout,
    loading,
  };

  if (loading) {
    return <div>Loading authentication...</div>; // Or a spinner
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};