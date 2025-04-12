import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Sparkles, TrendingUp, ArrowUpCircle } from "lucide-react";
import "./AiBotHero.css"

const HeroSection = () => {
  const [animateFinancial, setAnimateFinancial] = useState(false);
  
  useEffect(() => {
    // Trigger the animation after component mounts
    setTimeout(() => {
      setAnimateFinancial(true);
    }, 500);
  }, []);

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

      {/* 3D Financial Model with Animation */}
      <div className="hero-visual">
        <div className={`financial-model ${animateFinancial ? 'animate' : ''}`}>
          
          <div className="floating-circles">
            {[...Array(8)].map((_, index) => (
              <div 
                key={`circle-${index}`}
                className="floating-circle"
                style={{
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                  animationDelay: `${index * 0.3}s`,
                  animationDuration: `${3 + Math.random() * 4}s`
                }}
              >
                {index % 3 === 0 ? (
                  <ArrowUpCircle size={24} />
                ) : index % 3 === 1 ? (
                  <Sparkles size={20} />
                ) : (
                  '$'
                )}
              </div>
            ))}
          </div>
          
          <div className="glowing-sphere"></div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;