import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Menu, X } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './header.css';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [user, setUser] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();
  const [key, setKey] = useState(0);

  useEffect(() => {
    setKey(prev => prev + 1);
  }, [location]);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const getCookie = (name) => {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [key, value] = cookie.trim().split('=');
      if (key === name) return decodeURIComponent(value);
    }
    return null;
  };

  const fetchCSRFToken = async () => {
    await fetch("http://localhost:8000/csrf/", {
      method: "GET",
      credentials: "include",
    });
  };

  const handleLogout = async () => {
    try {
      await fetchCSRFToken();
      const csrfToken = getCookie("csrftoken");

      const res = await fetch("http://localhost:8000/logout/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      });

      if (res.ok) {
        localStorage.removeItem("user");
        localStorage.removeItem("token");
        setUser(null);
        navigate("/login");
        window.location.reload();
      } else {
        console.error("Logout failed:", await res.text());
      }
    } catch (err) {
      console.error("Error logging out:", err);
    }
  };

  return (
    <div>
      <motion.header
        key={key}
        className="header"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 80, delay: 0.3 }}
      >
        <div className="header-container">
          {/* Logo */}
          <div className="logo-container">
            <Link to="/" className="logo-text">
              Vect<span className="logo-highlight">ura</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="nav-desktop">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/chat" className="nav-link">Chat</Link>

            {user ? (
              <>
                <span className="welcome-text">Welcome, {user.name || "User"}</span>
                <button className="logout-button" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="login-button">Login</Link>
                <Link to="/SignUp" className="signup-button">Sign Up</Link>
              </>
            )}
          </nav>

          {/* Mobile Menu Button */}
          <button className="menu-button" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </motion.header>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="mobile-nav">
          <nav className="mobile-nav-inner">
            <Link to="/" className="nav-link" onClick={() => setIsMenuOpen(false)}>Home</Link>
            <Link to="/chat" className="nav-link" onClick={() => setIsMenuOpen(false)}>Chat</Link>

            {user ? (
              <>
                <span className="welcome-text">Welcome, {user.name || "User"}</span>
                <button className="logout-button" onClick={() => {
                  setIsMenuOpen(false);
                  handleLogout();
                }}>
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="login-button" onClick={() => setIsMenuOpen(false)}>Login</Link>
                <Link to="/SignUp" className="signup-button" onClick={() => setIsMenuOpen(false)}>Sign Up</Link>
              </>
            )}
          </nav>
        </div>
      )}
    </div>
  );
};

export default Header;