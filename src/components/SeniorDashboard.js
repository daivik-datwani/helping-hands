import React, { useState, useEffect } from 'react';
import './SeniorDashboard.css';

const SeniorDashboard = () => {
  const [user, setUser] = useState({
    name: 'John Doe',
    age: 72,
    location: 'Springfield'
  });

  const [upcomingRequests, setUpcomingRequests] = useState([
    { id: 1, type: 'Grocery Shopping', date: '2025-10-20', time: '10:00 AM', status: 'Pending' },
    { id: 2, type: 'Doctor Appointment', date: '2025-10-22', time: '2:00 PM', status: 'Confirmed' },
    { id: 3, type: 'House Cleaning', date: '2025-10-25', time: '9:00 AM', status: 'Pending' }
  ]);

  const [caregivers, setCaregivers] = useState([
    { id: 1, name: 'Sarah Johnson', availability: 'Available', rating: 4.8 },
    { id: 2, name: 'Michael Chen', availability: 'Busy', rating: 4.9 },
    { id: 3, name: 'Emily Rodriguez', availability: 'Available', rating: 4.7 }
  ]);

  return (
    <div className="senior-dashboard">
      {/* Welcome Banner */}
      <div className="welcome-banner">
        <h1 className="welcome-text">Welcome, {user.name}!</h1>
        <p className="welcome-subtitle">We're here to help you today</p>
      </div>

      {/* Profile Info Card */}
      <div className="profile-section">
        <div className="profile-card">
          <div className="profile-icon">👤</div>
          <div className="profile-details">
            <h2 className="profile-name">{user.name}</h2>
            <p className="profile-info">Age: {user.age}</p>
            <p className="profile-info">Location: {user.location}</p>
          </div>
        </div>
      </div>

      <div className="white-separator"></div>

      {/* Main Action Buttons */}
      <div className="action-buttons">
        <button className="large-action-button request-help-btn">
          <span className="button-icon">🆘</span>
          <span className="button-text">Request Help</span>
        </button>
        <button className="large-action-button view-caregivers-btn">
          <span className="button-icon">👥</span>
          <span className="button-text">View Caregivers</span>
        </button>
      </div>

      <div className="white-separator"></div>

      {/* Upcoming Requests Section */}
      <div className="requests-section">
        <h2 className="section-title">Your Upcoming Requests</h2>
        <div className="requests-container">
          {upcomingRequests.map((request) => (
            <div 
              key={request.id} 
              className={`request-card ${request.status === 'Confirmed' ? 'active-card' : ''}`}
            >
              <div className="request-type">{request.type}</div>
              <div className="request-details">
                <p className="request-date">📅 {request.date}</p>
                <p className="request-time">🕐 {request.time}</p>
              </div>
              <div className={`request-status status-${request.status.toLowerCase()}`}>
                {request.status}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="white-separator"></div>

      {/* Available Caregivers Section */}
      <div className="caregivers-section">
        <h2 className="section-title">Available Caregivers</h2>
        <div className="caregivers-container">
          {caregivers.map((caregiver) => (
            <div 
              key={caregiver.id} 
              className={`caregiver-card ${caregiver.availability === 'Available' ? 'active-card' : ''}`}
            >
              <div className="caregiver-avatar">👨‍⚕️</div>
              <div className="caregiver-info">
                <h3 className="caregiver-name">{caregiver.name}</h3>
                <p className="caregiver-rating">⭐ {caregiver.rating}/5.0</p>
                <div className={`caregiver-status status-${caregiver.availability.toLowerCase()}`}>
                  {caregiver.availability}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Emergency Contact Button */}
      <div className="emergency-section">
        <button className="emergency-button">
          <span className="button-icon">🚨</span>
          <span className="button-text">Emergency Contact</span>
        </button>
      </div>
    </div>
  );
};

export default SeniorDashboard;
