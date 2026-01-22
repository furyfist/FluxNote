import React from 'react';
import './Layout.css';

const Header: React.FC = () => {
    return (
        <header className="header">
            <div className="header-content">
                <h1 className="header-title">FluxNote</h1>
                <p className="header-subtitle">Syllabus to Video Playlist, Instantly</p>
            </div>
        </header>
    );
};

export default Header;
