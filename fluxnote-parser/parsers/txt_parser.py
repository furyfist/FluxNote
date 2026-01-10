# Plain text file parser

from typing import BinaryIO


def parse_txt(file: BinaryIO) -> str:
    """
    Parse plain text file.
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text content
    """
    content = file.read()
    
    # Try different encodings
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    
    # Fallback: decode with errors='ignore'
    return content.decode('utf-8', errors='ignore')
