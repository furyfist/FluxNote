// API Service for Lecture Matcher Backend
import { MatchRequest, MatchResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

/**
 * Match lectures from a YouTube playlist with syllabus topics
 */
export const matchLectures = async (
    playlistUrl: string,
    syllabus: string
): Promise<MatchResponse> => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                playlist_url: playlistUrl,
                syllabus_text: syllabus,
            } as MatchRequest),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                errorData.message || `API request failed with status ${response.status}`
            );
        }

        const data: MatchResponse = await response.json();
        return data;
    } catch (error) {
        // Network error or fetch failed
        if (error instanceof Error && error.message === 'Failed to fetch') {
            throw new Error(
                'Unable to connect to the server. Please ensure the backend is running on http://localhost:8000'
            );
        }
        throw error;
    }
};

/**
 * Health check for the API
 */
export const checkApiHealth = async (): Promise<boolean> => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
        });
        return response.ok;
    } catch (error) {
        return false;
    }
};
