// Validation Utilities

/**
 * Validates if a string is a valid YouTube playlist URL
 * @param {string} url - URL to validate
 * @returns {boolean} True if valid YouTube playlist URL
 */
export const validateYouTubePlaylistUrl = (url) => {
    if (!url || typeof url !== 'string') {
        return false;
    }

    // YouTube playlist URL patterns
    const playlistPatterns = [
        /^https?:\/\/(www\.)?youtube\.com\/playlist\?list=[\w-]+/,
        /^https?:\/\/(www\.)?youtube\.com\/watch\?.*list=[\w-]+/,
    ];

    return playlistPatterns.some((pattern) => pattern.test(url.trim()));
};

/**
 * Validates if syllabus text is not empty
 * @param {string} text - Syllabus text to validate
 * @returns {boolean} True if valid (not empty)
 */
export const validateSyllabus = (text) => {
    if (!text || typeof text !== 'string') {
        return false;
    }
    return text.trim().length > 0;
};

/**
 * Parses syllabus text into an array of topics
 * @param {string} syllabusText - Raw syllabus text
 * @returns {string[]} Array of topic strings
 */
export const parseTopics = (syllabusText) => {
    if (!syllabusText) {
        return [];
    }

    return syllabusText
        .split('\n')
        .map((line) => line.trim())
        .filter((line) => line.length > 0);
};

/**
 * Validates form data before submission
 * @param {string} playlistUrl - YouTube playlist URL
 * @param {string} syllabus - Syllabus text
 * @returns {Object} Validation result with isValid flag and errors object
 */
export const validateFormData = (playlistUrl, syllabus) => {
    const errors = {};

    if (!playlistUrl || !playlistUrl.trim()) {
        errors.playlistUrl = 'Please enter a YouTube playlist URL';
    } else if (!validateYouTubePlaylistUrl(playlistUrl)) {
        errors.playlistUrl = 'Please enter a valid YouTube playlist URL';
    }

    if (!syllabus || !syllabus.trim()) {
        errors.syllabus = 'Please enter your syllabus topics';
    } else if (parseTopics(syllabus).length === 0) {
        errors.syllabus = 'Please enter at least one topic';
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors,
    };
};

/**
 * Formats a similarity score for display
 * @param {number} score - Score value (0-1)
 * @returns {string} Formatted percentage string
 */
export const formatScore = (score) => {
    return `${Math.round(score * 100)}%`;
};

/**
 * Gets score category based on value
 * @param {number} score - Score value (0-1)
 * @returns {string} Category: 'high', 'medium', or 'low'
 */
export const getScoreCategory = (score) => {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
};
