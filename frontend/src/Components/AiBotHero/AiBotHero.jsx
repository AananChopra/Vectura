import React from "react";
import { LockIcon } from "lucide-react";
import { Link } from "react-router-dom";
import "./AibotHero.css"

const HeroSection = () => {
  return (
    <div className="hero-container">
      <div className="hero-content">
        <div className="text-center">
          <h1 className="hero-title">
            Meet Vectura, Your AI Financial Assistant
          </h1>
          <p className="hero-description mx-auto">
            Ask questions, get personalized debt elimination strategies, and receive step-by-step guidance 
            without the complex financial jargon. Your path to financial freedom starts with a simple conversation.
          </p>
          
          <div className="hero-buttons justify-content-center">
            <Link to="/chat" className="btn Aibtn-primary">Chat with Vectura</Link>
            <Link to="/home" className="btn Aibtn-outline">Home</Link>
         </div>

        </div>
      </div>
      
      <div className="debt-summary-card">
        <div className="card-header">
          <LockIcon size={20} />
          <h2>Debt Summary</h2>
        </div>
        
        <div className="card-body">
          <div className="summary-item">
            <div className="summary-label">TOTAL DEBT</div>
            <div className="summary-value-container">
              <div className="summary-dot"></div>
              <div className="summary-value">$24,500</div>
            </div>
          </div>
          
          <div className="summary-item">
            <div className="summary-label">AVG. INTEREST RATE</div>
            <div className="summary-value-container">
              <div className="summary-dot"></div>
              <div className="summary-value">16.2%</div>
            </div>
          </div>
          
          <div className="summary-item">
            <div className="summary-label">PAYOFF TIMELINE</div>
            <div className="summary-value-container">
              <div className="summary-dot"></div>
              <div className="summary-value">3.5 years</div>
            </div>
          </div>
          
          <button className="optimization-btn">Get AI Analysis Now</button>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;