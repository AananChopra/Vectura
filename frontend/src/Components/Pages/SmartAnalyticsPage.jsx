// FinancialDashboard.jsx
import React from 'react';
import UserInfoCard from '../UserInfoCard/UserInfoCard';
import Header from "../Header/Header"
import DebtAssessmentCard from '../DebtAssessmentCard/DebtAssessmentCard';
import SpendingHabitsCard from '../SpendingHabitsCard/SpendingHabitsCard';
import AIRecommendationsCard from "../AIRecommendationCard/AIRecommendationsCard";
import './SmartAnalyticsPage.css';

function FinancialDashboard() {
  return (
    <div>
      <Header/> 
      <div className="financial-dashboard">
        <header className="dashboard-header">
            <h1>Financial Dashboard</h1>
        </header>
        
        <div className="dashboard-grid">
            <UserInfoCard />
            <DebtAssessmentCard />
            <SpendingHabitsCard />
            <AIRecommendationsCard />
        </div>
      </div>
    </div>
  );
}

export default FinancialDashboard;