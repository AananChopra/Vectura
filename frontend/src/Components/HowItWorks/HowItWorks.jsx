import React from 'react';
import { Link } from 'react-router-dom';
import './HowItWorks.css'; // Import the CSS file for the How It Works section

const HowItWorksSection = () => {
  return (
    <section id="how-it-works" className="how-it-works-section">
      <div className="howitworks-container">
        <h2 className="section-title">
          How <span className="gradient-text">Vectura</span> Works
        </h2>

        <div className="steps-grid">
          <div className="step">
            <div className="step-icon step-1">
              <span className="step-number">1</span>
            </div>
            <h3 className="step-title">Chat With AI</h3>
            <p className="step-description">
              Start a conversation with our AI assistant about your debt situation and financial goals.
            </p>
          </div>

          <div className="step">
            <div className="step-icon step-2">
              <span className="step-number">2</span>
            </div>
            <h3 className="step-title">Get Personalized Plans</h3>
            <p className="step-description">
              Receive custom debt management strategies based on your specific financial situation.
            </p>
          </div>

          <div className="step">
            <div className="step-icon step-3">
              <span className="step-number">3</span>
            </div>
            <h3 className="step-title">Track Your Progress</h3>
            <p className="step-description">
              Follow your debt payoff progress and adjust your strategy as your situation changes.
            </p>
          </div>
        </div>

        <div className="cta-container">
          <p className="cta-description">
            DebtAlly combines the power of AI with proven financial strategies to help you pay off debt faster, save on interest, and achieve financial freedom.
          </p>
          <Link 
            to="/chat" 
            className="cta-btn"
          >
            Start Your Debt-Free Journey
          </Link>
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
