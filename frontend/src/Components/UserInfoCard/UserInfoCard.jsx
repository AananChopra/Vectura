// UserInfoCard.jsx
import React from 'react';
import './UserInfoCard.css';

// Sample user data - in a real application, this would come from props or context
const userData = {
  name: "John Doe",
  age: 32,
  income: 65000,
  totalDebt: 28500,
  creditScore: 680
};

function UserInfoCard() {
  return (
    <div className="user-info-card">
      <div className="card-header">
        <span className="icon">👤</span>
        <h2>User Information</h2>
      </div>
      <div className="user-info-grid">
        <div className="info-item">
          <p className="label">Name</p>
          <p className="value">{userData.name}</p>
        </div>
        <div className="info-item">
          <p className="label">Age</p>
          <p className="value">{userData.age}</p>
        </div>
        <div className="info-item">
          <p className="label">Annual Income</p>
          <p className="value">${userData.income.toLocaleString()}</p>
        </div>
        <div className="info-item">
          <p className="label">Credit Score</p>
          <p className="value">{userData.creditScore}</p>
        </div>
      </div>
    </div>
  );
}

export default UserInfoCard;