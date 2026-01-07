import React, { useState } from 'react';
import { validateFormData } from '../../utils/validation';
import './MatchForm.css';

const MatchForm = ({ onSubmit, isLoading }) => {
    const [playlistUrl, setPlaylistUrl] = useState('');
    const [syllabus, setSyllabus] = useState('');
    const [errors, setErrors] = useState({});

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate form data
        const validation = validateFormData(playlistUrl, syllabus);

        if (!validation.isValid) {
            setErrors(validation.errors);
            return;
        }

        // Clear errors and submit
        setErrors({});
        onSubmit({ playlistUrl, syllabus });
    };

    const handlePlaylistUrlChange = (e) => {
        setPlaylistUrl(e.target.value);
        // Clear error when user starts typing
        if (errors.playlistUrl) {
            setErrors((prev) => ({ ...prev, playlistUrl: '' }));
        }
    };

    const handleSyllabusChange = (e) => {
        setSyllabus(e.target.value);
        // Clear error when user starts typing
        if (errors.syllabus) {
            setErrors((prev) => ({ ...prev, syllabus: '' }));
        }
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit} className="match-form">
                <div className="form-group">
                    <label htmlFor="playlistUrl" className="form-label">
                        YouTube Playlist URL
                    </label>
                    <input
                        type="text"
                        id="playlistUrl"
                        className={`input ${errors.playlistUrl ? 'error' : ''}`}
                        placeholder="https://www.youtube.com/playlist?list=..."
                        value={playlistUrl}
                        onChange={handlePlaylistUrlChange}
                        disabled={isLoading}
                    />
                    {errors.playlistUrl && (
                        <p className="error-text">{errors.playlistUrl}</p>
                    )}
                    <p className="form-help">
                        Enter the full URL of the YouTube playlist containing your lectures
                    </p>
                </div>

                <div className="form-group">
                    <label htmlFor="syllabus" className="form-label">
                        Syllabus Topics
                    </label>
                    <textarea
                        id="syllabus"
                        className={`input textarea ${errors.syllabus ? 'error' : ''}`}
                        placeholder="Introduction to Databases&#10;SQL Basics&#10;Normalization&#10;Transactions and Concurrency"
                        value={syllabus}
                        onChange={handleSyllabusChange}
                        disabled={isLoading}
                        rows={10}
                    />
                    {errors.syllabus && (
                        <p className="error-text">{errors.syllabus}</p>
                    )}
                    <p className="form-help">
                        Enter one topic per line. Each topic will be matched with lectures from the playlist.
                    </p>
                </div>

                <button
                    type="submit"
                    className="btn btn-primary submit-btn"
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <>
                            <span className="btn-spinner"></span>
                            Processing...
                        </>
                    ) : (
                        <>
                            <span className="btn-icon">🔍</span>
                            Match Lectures
                        </>
                    )}
                </button>
            </form>
        </div>
    );
};

export default MatchForm;
