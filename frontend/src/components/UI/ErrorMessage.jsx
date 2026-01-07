import React from 'react';
import './UI.css';

const ErrorMessage = ({ message, onRetry }) => {
    return (
        <div className="error-container fade-in">
            <div className="error-icon">
                <svg
                    width="48"
                    height="48"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                >
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
            </div>
            <h3 className="error-title">Oops! Something went wrong</h3>
            <p className="error-message">{message}</p>
            {onRetry && (
                <button className="btn btn-primary" onClick={onRetry}>
                    Try Again
                </button>
            )}
        </div>
    );
};

export default ErrorMessage;
