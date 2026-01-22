import React, { useState } from 'react';
import Header from './components/Layout/Header';
import MatchForm from './components/Form/MatchForm';
import ResultsDisplay from './components/Results/ResultsDisplay';
import LoadingSpinner from './components/UI/LoadingSpinner';
import ErrorMessage from './components/UI/ErrorMessage';
import { matchLectures } from './services/api';
import { FormData, TopicResult } from './types';
import './App.css';

function App() {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [results, setResults] = useState<TopicResult[] | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFormSubmit = async (formData: FormData) => {
        setIsLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await matchLectures(formData.playlistUrl, formData.syllabus);

            if (response.success && response.matches) {
                setResults(response.matches);
            } else {
                setError('No results returned from the server. Please try again.');
            }
        } catch (err) {
            const errorMessage = err instanceof Error
                ? err.message
                : 'An unexpected error occurred. Please try again.';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    const handleRetry = () => {
        setError(null);
        setResults(null);
    };

    return (
        <div className="app">
            <Header />

            <main className="main-content">
                <div className="content-grid">
                    <div className="input-section">
                        <MatchForm onSubmit={handleFormSubmit} isLoading={isLoading} />
                    </div>

                    <div className="results-section">
                        {isLoading && <LoadingSpinner />}

                        {error && <ErrorMessage message={error} onRetry={handleRetry} />}

                        {results && !isLoading && !error && (
                            <ResultsDisplay matches={results} />
                        )}

                        {!results && !isLoading && !error && (
                            <div className="empty-state">
                                <div className="empty-state-icon">
                                    <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                                        <rect x="10" y="15" width="60" height="45" rx="4" stroke="#CBD2DC" strokeWidth="2" fill="none" />
                                        <rect x="15" y="20" width="20" height="15" rx="2" fill="#E4E9F0" />
                                        <rect x="40" y="20" width="25" height="3" rx="1.5" fill="#E4E9F0" />
                                        <rect x="40" y="27" width="20" height="3" rx="1.5" fill="#E4E9F0" />
                                        <rect x="15" y="40" width="20" height="15" rx="2" fill="#E4E9F0" />
                                        <rect x="40" y="40" width="25" height="3" rx="1.5" fill="#E4E9F0" />
                                        <rect x="40" y="47" width="20" height="3" rx="1.5" fill="#E4E9F0" />
                                        <circle cx="40" cy="40" r="15" fill="#4A90E2" opacity="0.1" />
                                        <path d="M40 32L44 36L40 40L36 36L40 32Z" fill="#4A90E2" opacity="0.3" />
                                    </svg>
                                </div>
                                <p className="empty-state-text">Your AI-matched video list will appear here.</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
