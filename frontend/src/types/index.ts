// Type Definitions for FluxNote Application

// API Types
export interface MatchRequest {
    playlist_url: string;
    syllabus: string;
}

export interface Lecture {
    title: string;
    video_id: string;
    url: string;
}

export interface Match {
    lecture: Lecture;
    score: number;
}

export interface TopicResult {
    topic: string;
    matches: Match[];
}

export interface MatchResponse {
    success: boolean;
    results: TopicResult[];
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
    results: TopicResult[];
}

export interface TopicSectionProps {
    topic: string;
    matches: Match[];
}

export interface LectureCardProps {
    lecture: Lecture;
    score: number;
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
