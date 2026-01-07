// API Service for Lecture Matcher Backend

const API_BASE_URL = 'http://localhost:5000';

/**
 * Match lectures from a YouTube playlist with syllabus topics
 * @param {string} playlistUrl - YouTube playlist URL
 * @param {string} syllabus - Syllabus text (one topic per line)
 * @returns {Promise<Object>} API response with matching results
 */
export const matchLectures = async (playlistUrl, syllabus) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/match`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        playlist_url: playlistUrl,
        syllabus: syllabus,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `API request failed with status ${response.status}`
      );
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // Network error or fetch failed
    if (error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please ensure the backend is running on http://localhost:5000'
      );
    }
    throw error;
  }
};

/**
 * Health check for the API
 * @returns {Promise<boolean>} True if API is reachable
 */
export const checkApiHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
    });
    return response.ok;
  } catch (error) {
    return false;
  }
};
