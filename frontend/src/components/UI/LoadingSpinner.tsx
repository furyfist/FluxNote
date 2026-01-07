import React from 'react';
import './UI.css';
import { LoadingSpinnerProps } from '../../types';

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
    message = 'Processing your request...'
}) => {
    return (
        <div className="loading-container fade-in">
            <div className="spinner-wrapper">
                <div className="spinner"></div>
            </div>
            <p className="loading-message">{message}</p>
            <p className="loading-submessage">
                This may take a few moments while we analyze the playlist and match lectures
            </p>
        </div>
    );
};

export default LoadingSpinner;
