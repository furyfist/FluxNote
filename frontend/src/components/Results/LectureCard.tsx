import React from 'react';
import ScoreBadge from '../UI/ScoreBadge';
import './Results.css';
import { LectureCardProps } from '../../types';

const LectureCard: React.FC<LectureCardProps> = ({ lecture, score }) => {
    return (
        <div className="lecture-card">
            <div className="lecture-card-header">
                <a
                    href={lecture.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="lecture-link"
                >
                    <span className="youtube-icon">▶️</span>
                    <span className="lecture-title">{lecture.title}</span>
                </a>
            </div>
            <div className="lecture-card-footer">
                <ScoreBadge score={score} />
                <span className="match-label">Match Score</span>
            </div>
        </div>
    );
};

export default LectureCard;
