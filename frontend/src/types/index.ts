// Type Definitions for FluxNote Application

// API Types
export interface MatchRequest {
    playlist_url: string;
    syllabus_text: string;
}

export interface MatchedLecture {
    title: string;
    url: string;
    reasoning: string;
    confidence: number;
    order: number;
}

export interface TopicResult {
    topic: string;
    matched_lectures: MatchedLecture[];
}

export interface MatchResponse {
    success: boolean;
    matches: TopicResult[];
    message?: string;
}

// Form Types
export interface FormData {
    playlistUrl: string;
    syllabus: string;
}

export interface ValidationErrors {
    playlistUrl?: string;
    syllabus?: string;
}

export interface ValidationResult {
    isValid: boolean;
    errors: ValidationErrors;
}

// Component Props Types
export interface MatchFormProps {
    onSubmit: (data: FormData) => void;
    isLoading: boolean;
}

export interface ResultsDisplayProps {
    matches: TopicResult[];
}

export interface TopicSectionProps {
    topic: string;
    matches: MatchedLecture[];
}

export interface LectureCardProps {
    lecture: MatchedLecture;
}

export interface LoadingSpinnerProps {
    message?: string;
}

export interface ErrorMessageProps {
    message: string;
    onRetry?: () => void;
}

export interface ScoreBadgeProps {
    score: number;
}

// Utility Types
export type ScoreCategory = 'high' | 'medium' | 'low';
