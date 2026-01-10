# File type validation using magic numbers

import magic
from typing import BinaryIO


def validate_file_type(file: BinaryIO, allowed_types: list[str] = None) -> tuple[bool, str]:
    """
    Validate file type using magic numbers (file signature).
    
    Args:
        file: Binary file object
        allowed_types: List of allowed MIME types (optional)
        
    Returns:
        Tuple of (is_valid, detected_mime_type)
    """
    if allowed_types is None:
        allowed_types = [
            'text/plain',
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/png',
            'image/jpeg'
        ]
    
    # Read file content for magic number detection
    file.seek(0)
    file_content = file.read(2048)  # Read first 2KB for detection
    file.seek(0)  # Reset file pointer
    
    # Detect MIME type
    mime = magic.from_buffer(file_content, mime=True)
    
    # Validate against allowed types
    is_valid = mime in allowed_types
    
    return is_valid, mime


def get_file_extension(mime_type: str) -> str:
    """
    Get file extension from MIME type.
    
    Args:
        mime_type: MIME type string
        
    Returns:
        File extension (with dot)
    """
    mime_to_ext = {
        'text/plain': '.txt',
        'application/pdf': '.pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'image/png': '.png',
        'image/jpeg': '.jpg'
    }
    
    return mime_to_ext.get(mime_type, '')
