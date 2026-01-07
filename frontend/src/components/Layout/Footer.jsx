import React from 'react';
import './Layout.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container">
                <p className="footer-text">
                    © {new Date().getFullYear()} Lecture Matcher. Built with React.
                </p>
            </div>
        </footer>
    );
};

export default Footer;
