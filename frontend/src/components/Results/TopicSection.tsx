import React from 'react';
import LectureCard from './LectureCard';
import './Results.css';
import { TopicSectionProps } from '../../types';

const TopicSection: React.FC<TopicSectionProps> = ({ topic, matches }) => {
    return (
        <div className="topic-section fade-in">
            <h3 className="topic-title">{topic}</h3>
            {matches && matches.length > 0 ? (
                <div className="lectures-grid">
                    {matches.map((match, index) => (
                        <LectureCard
                            key={`${match.lecture.video_id}-${index}`}
                            lecture={match.lecture}
                            score={match.score}
                        />
                    ))}
                </div>
            ) : (
                <div className="no-matches">
                    <span className="no-matches-icon">🔍</span>
                    <p className="no-matches-text">No matches found for this topic</p>
                </div>
            )}
        </div>
    );
};

export default TopicSection;
