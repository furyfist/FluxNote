import React from 'react';
import { formatScore, getScoreCategory } from '../../utils/validation';
import './UI.css';

const ScoreBadge = ({ score }) => {
    const category = getScoreCategory(score);
    const formattedScore = formatScore(score);

    return (
        <span className={`score-badge score-badge-${category}`}>
            {formattedScore}
        </span>
    );
};

export default ScoreBadge;
