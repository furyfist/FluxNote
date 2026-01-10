# Text cleaning utilities

import re


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excess whitespace and newlines.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove multiple consecutive newlines (keep max 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove multiple consecutive spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove trailing/leading whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove empty lines at start and end
    text = text.strip()
    
    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize all whitespace to single spaces.
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized whitespace
    """
    # Replace all whitespace (including newlines, tabs) with single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.
    
    Args:
        text: Input text
        keep_punctuation: Whether to keep basic punctuation marks
        
    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?;:\-\'"()]', '', text)
    else:
        # Keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text
