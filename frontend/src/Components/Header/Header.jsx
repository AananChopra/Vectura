import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Menu, X } from 'lucide-react';
import { Link } from 'react-router-dom';
import './header.css';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="header">
      <motion.div className="header-container"
        initial={{ y: -100, opacity: 0 }} // Starts from above the screen
        animate={{ y: 0, opacity: 1 }} // Moves into position when in view
        viewport={{ once: true }} // Animates only once when it comes into view
        transition={{ type: 'spring', stiffness: 80, delay: 0.3 }} // Smooth animation
      >
        {/* Logo */}
        <div className="logo-container">
          <Link to="/" className="logo-text">
            Vect<span className="logo-highlight">ura</span>
          </Link>
        </div>

        {/* Desktop Navigation Bar */}
        <nav className="nav-desktop">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/features" className="nav-link">Features</Link>
          <Link to="/how-it-works" className="nav-link">How It Works</Link>
          <Link to="/chat" className="nav-link">Chat</Link>
          <Link to="/SignUp" className="signup-button">Sign Up</Link>
        </nav>

        {/* Mobile Menu Button */}
        <button className="menu-button" onClick={() => setIsMenuOpen(!isMenuOpen)}>
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </motion.div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="mobile-nav">
          <nav className="mobile-nav-inner">
            <Link to="/" className="nav-link" onClick={() => setIsMenuOpen(false)}>Home</Link>
            <Link to="/features" className="nav-link" onClick={() => setIsMenuOpen(false)}>Features</Link>
            <Link to="/how-it-works" className="nav-link" onClick={() => setIsMenuOpen(false)}>How It Works</Link>
            <Link to="/chat" className="nav-link" onClick={() => setIsMenuOpen(false)}>Chat</Link>
            <Link to="/SignUp" className="signup-button" onClick={() => setIsMenuOpen(false)}>Sign Up</Link>
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;
