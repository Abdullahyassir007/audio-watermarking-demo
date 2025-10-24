import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import AboutPage from './pages/AboutPage'
import EncodePage from './pages/EncodePage'
import DecodePage from './pages/DecodePage'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 flex flex-col">
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        
        <Routes>
          <Route path="/" element={<HomePage isAuthenticated={isAuthenticated} />} />
          <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
          <Route path="/about" element={<AboutPage />} />
          <Route
            path="/encode"
            element={isAuthenticated ? <EncodePage /> : <Navigate to="/login" replace />}
          />
          <Route
            path="/decode"
            element={isAuthenticated ? <DecodePage /> : <Navigate to="/login" replace />}
          />
        </Routes>

        <Footer />
      </div>
    </Router>
  )
}

export default App
