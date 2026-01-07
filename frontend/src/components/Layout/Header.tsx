import React from 'react';
import './Layout.css';

const Header: React.FC = () => {
    return (
        <header className="header">
            <div className="container">
                <div className="header-content">
                    <h1 className="header-title">
                        <span className="header-icon">🎓</span>
                        FluxNote
                    </h1>
                    <p className="header-subtitle">
                        Match YouTube lectures with your syllabus topics
                    </p>
                </div>
            </div>
        </header>
    );
};

export default Header;
