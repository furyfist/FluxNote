import React from 'react';
import TopicSection from './TopicSection';
import './Results.css';
import { ResultsDisplayProps } from '../../types';

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ matches }) => {
    if (!matches || matches.length === 0) {
        return null;
    }

    return (
        <div className="results-container">
            <div className="results-header">
                <h2 className="results-title">Your Curated Playlist</h2>
            </div>

            <div className="results-content">
                {matches.map((result, index) => (
                    <TopicSection
                        key={`${result.topic}-${index}`}
                        topic={result.topic}
                        matches={result.matched_lectures}
                    />
                ))}
            </div>
        </div>
    );
};

export default ResultsDisplay;
