import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, DollarSign, BadgePercent } from 'lucide-react';
import './Hero.css'; // Import the CSS file for the Hero Section

const HeroSection = () => {
  return (
    <section className="hero-section">
      <div className="container">
        <div className="text-container">
          <h1 className="hero-title">AI-Powered Debt Management Made Simple</h1>
          <p className="hero-description">
            Chat with our AI assistant to get personalized strategies for managing and eliminating your debt faster.
          </p>
          <div className="cta-buttons">
            <Link to="/chat" className="cta-btn-1">
              Try It Now
            </Link>
            <Link to="/Home" className="cta-btn-2">
              Learn More
            </Link>
          </div>
        </div>
        <div className="summary-container">
          <div className="debt-summary-card">
            <div className="debt-summary-header">
              <h3 className="debt-summary-title">Debt Summary</h3>
            </div>
            <div className="debt-summary-body">
              <div className="debt-item">
                <DollarSign className="debt-icon" />
                <div className="debt-info">
                  <h4 className="debt-label">Total Debt</h4>
                  <p className="debt-value">$24,500</p>
                </div>
              </div>
              <div className="debt-item">
                <BadgePercent className="debt-icon" />
                <div className="debt-info">
                  <h4 className="debt-label">Avg. Interest Rate</h4>
                  <p className="debt-value">16.2%</p>
                </div>
              </div>
              <div className="debt-item">
                <TrendingUp className="debt-icon" />
                <div className="debt-info">
                  <h4 className="debt-label">Payoff Timeline</h4>
                  <p className="debt-value">3.5 years</p>
                </div>
              </div>
              <Link to="/chat" className="get-plan-btn">
                Get Optimization Plan
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
