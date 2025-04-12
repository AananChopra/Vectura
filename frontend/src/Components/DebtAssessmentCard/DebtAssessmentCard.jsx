// DebtAssessmentCard.jsx
import React from 'react';
import './DebtAssessmentCard.css';

// Sample user data - in a real application, this would come from props or context
const userData = {
  name: "John Doe",
  age: 32,
  income: 65000,
  totalDebt: 28500,
  creditScore: 680
};

function DebtAssessmentCard() {
  // Calculate debt-to-income ratio
  const debtToIncomeRatio = ((userData.totalDebt / userData.income) * 100).toFixed(1);
  
  // Determine debt condition based on debt-to-income ratio
  let debtCondition = "Healthy";
  let statusClass = "status-healthy";
  
  if (debtToIncomeRatio > 35) {
    debtCondition = "Critical";
    statusClass = "status-critical";
  } else if (debtToIncomeRatio > 20) {
    debtCondition = "Concerning";
    statusClass = "status-concerning";
  }
  
  return (
    <div className="debt-assessment-card">
      <div className="card-header">
        <span className="icon">⚠️</span>
        <h2>Debt Assessment</h2>
      </div>
      
      <div className="metric-item">
        <p className="label">Total Debt</p>
        <p className="value large">${userData.totalDebt.toLocaleString()}</p>
      </div>
      
      <div className="metric-item">
        <p className="label">Debt-to-Income Ratio</p>
        <p className="value large">{debtToIncomeRatio}%</p>
      </div>
      
      <div className="metric-item">
        <p className="label">Status</p>
        <p className={`value status ${statusClass}`}>{debtCondition}</p>
        <p className="description">
          {debtCondition === "Critical" ? 
            "Your debt level is significantly high compared to your income. Immediate action is recommended." :
            debtCondition === "Concerning" ?
            "Your debt is higher than recommended. Consider debt reduction strategies." :
            "Your debt is at a manageable level relative to your income."
          }
        </p>
      </div>
    </div>
  );
}

export default DebtAssessmentCard;