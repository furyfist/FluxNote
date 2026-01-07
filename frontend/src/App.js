import React, { useState } from 'react';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import MatchForm from './components/Form/MatchForm';
import ResultsDisplay from './components/Results/ResultsDisplay';
import LoadingSpinner from './components/UI/LoadingSpinner';
import ErrorMessage from './components/UI/ErrorMessage';
import { matchLectures } from './services/api';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFormSubmit = async ({ playlistUrl, syllabus }) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await matchLectures(playlistUrl, syllabus);

      if (response.success && response.results) {
        setResults(response.results);
      } else {
        setError('No results returned from the server. Please try again.');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.');
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
        <div className="container">
          <MatchForm onSubmit={handleFormSubmit} isLoading={isLoading} />

          {isLoading && <LoadingSpinner />}

          {error && <ErrorMessage message={error} onRetry={handleRetry} />}

          {results && !isLoading && !error && (
            <ResultsDisplay results={results} />
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
