// SpendingHabitsCard.jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './SpendingHabitsCard.css';

// Sample data for spending categories
const spendingCategories = [
  { name: 'Housing', value: 1400, color: '#0088FE' },
  { name: 'Transportation', value: 450, color: '#00C49F' },
  { name: 'Food', value: 650, color: '#FFBB28' },
  { name: 'Entertainment', value: 300, color: '#FF8042' },
  { name: 'Debt Payments', value: 800, color: '#8884d8' },
  { name: 'Others', value: 200, color: '#82ca9d' },
];

// Sample data for monthly expenses
const monthlyExpenses = [
  { month: 'Jan', expenses: 3200, income: 5400 },
  { month: 'Feb', expenses: 3600, income: 5400 },
  { month: 'Mar', expenses: 3100, income: 5400 },
  { month: 'Apr', expenses: 3800, income: 5400 },
  { month: 'May', expenses: 3400, income: 5500 },
  { month: 'Jun', expenses: 3200, income: 5500 },
];

function SpendingHabitsCard() {
  // Custom label for pie chart segments
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="spending-habits-card">
      <div className="card-header">
        <span className="icon">💳</span>
        <h2>Spending Habits</h2>
      </div>
      
      <div className="chart-section">
        <h3>Monthly Spending Breakdown</h3>
        <div className="pie-chart-container">
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={spendingCategories}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={renderCustomizedLabel}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {spendingCategories.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `$${value}`} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        <div className="legend-container">
          {spendingCategories.map((category, index) => (
            <div key={index} className="legend-item">
              <div className="color-indicator" style={{ backgroundColor: category.color }}></div>
              <span>{category.name}: ${category.value}</span>
            </div>
          ))}
        </div>
      </div>
      
      <div className="chart-section">
        <h3>Monthly Expenses vs Income</h3>
        <div className="line-chart-container">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={monthlyExpenses}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value}`} />
              <Legend />
              <Line type="monotone" dataKey="expenses" stroke="#ff7300" name="Expenses" />
              <Line type="monotone" dataKey="income" stroke="#387908" name="Income" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default SpendingHabitsCard;