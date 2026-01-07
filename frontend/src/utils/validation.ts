// Validation Utilities
import { ValidationErrors, ValidationResult, ScoreCategory } from '../types';

/**
 * Validates if a string is a valid YouTube playlist URL
 */
export const validateYouTubePlaylistUrl = (url: string): boolean => {
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
 */
export const validateSyllabus = (text: string): boolean => {
    if (!text || typeof text !== 'string') {
        return false;
    }
    return text.trim().length > 0;
};

/**
 * Parses syllabus text into an array of topics
 */
export const parseTopics = (syllabusText: string): string[] => {
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
 */
export const validateFormData = (
    playlistUrl: string,
    syllabus: string
): ValidationResult => {
    const errors: ValidationErrors = {};

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
 */
export const formatScore = (score: number): string => {
    return `${Math.round(score * 100)}%`;
};

/**
 * Gets score category based on value
 */
export const getScoreCategory = (score: number): ScoreCategory => {
    if (score >= 0.7) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
};
