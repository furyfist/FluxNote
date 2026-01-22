import React, { useState, FormEvent, ChangeEvent } from 'react';
import { validateFormData } from '../../utils/validation';
import './MatchForm.css';
import { MatchFormProps, ValidationErrors } from '../../types';

const MatchForm: React.FC<MatchFormProps> = ({ onSubmit, isLoading }) => {
    const [playlistUrl, setPlaylistUrl] = useState<string>('');
    const [syllabus, setSyllabus] = useState<string>('');
    const [errors, setErrors] = useState<ValidationErrors>({});

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
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

    const handlePlaylistUrlChange = (e: ChangeEvent<HTMLInputElement>) => {
        setPlaylistUrl(e.target.value);
        // Clear error when user starts typing
        if (errors.playlistUrl) {
            setErrors((prev) => ({ ...prev, playlistUrl: undefined }));
        }
    };

    const handleSyllabusChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        setSyllabus(e.target.value);
        // Clear error when user starts typing
        if (errors.syllabus) {
            setErrors((prev) => ({ ...prev, syllabus: undefined }));
        }
    };

    return (
        <div className="form-card">
            <h2 className="form-card-title">Input</h2>
            <form onSubmit={handleSubmit} className="match-form">
                <div className="form-group">
                    <label htmlFor="syllabus" className="form-label">
                        1. Paste Syllabus Text
                    </label>
                    <textarea
                        id="syllabus"
                        className={`input textarea ${errors.syllabus ? 'error' : ''}`}
                        placeholder="e.g., Topics: Linear Regression, Gradient Descent, Neural Networks..."
                        value={syllabus}
                        onChange={handleSyllabusChange}
                        disabled={isLoading}
                        rows={8}
                    />
                    {errors.syllabus && (
                        <p className="error-text">{errors.syllabus}</p>
                    )}
                </div>

                <div className="form-group">
                    <label htmlFor="playlistUrl" className="form-label">
                        2. Paste YouTube Playlist URL
                    </label>
                    <div className="input-with-icon">
                        <svg className="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 0C4.477 0 0 4.477 0 10C0 15.523 4.477 20 10 20C15.523 20 20 15.523 20 10C20 4.477 15.523 0 10 0ZM13.5 10.5L8.5 13.5V7.5L13.5 10.5Z" fill="#9CA6B8" />
                        </svg>
                        <input
                            type="text"
                            id="playlistUrl"
                            className={`input input-with-padding ${errors.playlistUrl ? 'error' : ''}`}
                            placeholder="https://youtube.com/playlist?list=..."
                            value={playlistUrl}
                            onChange={handlePlaylistUrlChange}
                            disabled={isLoading}
                        />
                    </div>
                    {errors.playlistUrl && (
                        <p className="error-text">{errors.playlistUrl}</p>
                    )}
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
                        'Generate Playlist'
                    )}
                </button>
            </form>
        </div>
    );
};

export default MatchForm;
