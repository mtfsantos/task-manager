import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginPage from './components/Login';
import DashboardPage from './pages/DashboardPage';
import HomePage from './pages/HomePage';
import Layout from './components/Layout';

// PrivateRoute component to protect routes
const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<HomePage />} /> {/* Or redirect directly to /dashboard if logged in */}
            <Route 
              path="/dashboard" 
              element={
                <PrivateRoute>
                  <DashboardPage />
                </PrivateRoute>
              } 
            />
            {/* Add more routes here as needed */}
          </Routes>
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;