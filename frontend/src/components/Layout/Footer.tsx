import React from 'react';
import './Layout.css';

const Footer: React.FC = () => {
    return (
        <footer className="footer">
            <div className="container">
                <p className="footer-text">
                    © {new Date().getFullYear()} FluxNote. Built with React & TypeScript.
                </p>
            </div>
        </footer>
    );
};

export default Footer;
