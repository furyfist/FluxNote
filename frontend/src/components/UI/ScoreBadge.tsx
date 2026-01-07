import React from 'react';
import { formatScore, getScoreCategory } from '../../utils/validation';
import './UI.css';
import { ScoreBadgeProps } from '../../types';

const ScoreBadge: React.FC<ScoreBadgeProps> = ({ score }) => {
    const category = getScoreCategory(score);
    const formattedScore = formatScore(score);

    return (
        <span className={`score-badge score-badge-${category}`}>
            {formattedScore}
        </span>
    );
};

export default ScoreBadge;
