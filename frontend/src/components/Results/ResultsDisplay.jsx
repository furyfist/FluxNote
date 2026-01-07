import React from 'react';
import TopicSection from './TopicSection';
import './Results.css';

const ResultsDisplay = ({ results }) => {
    if (!results || results.length === 0) {
        return null;
    }

    return (
        <div className="results-container">
            <div className="results-header">
                <h2 className="results-title">
                    <span className="results-icon">✨</span>
                    Matching Results
                </h2>
                <p className="results-subtitle">
                    Found {results.length} topic{results.length !== 1 ? 's' : ''} with matching lectures
                </p>
            </div>

            <div className="results-content">
                {results.map((result, index) => (
                    <TopicSection
                        key={`${result.topic}-${index}`}
                        topic={result.topic}
                        matches={result.matches}
                    />
                ))}
            </div>
        </div>
    );
};

export default ResultsDisplay;
