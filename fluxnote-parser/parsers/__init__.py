# Logic to pick the right parser based on file type

from typing import BinaryIO


def get_parser(file_type: str):
    """
    Returns the appropriate parser based on file type.
    
    Args:
        file_type: The MIME type or extension of the file
        
    Returns:
        The parser function for the given file type
    """
    if file_type in ['text/plain', '.txt']:
        from .txt_parser import parse_txt
        return parse_txt
    elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx']:
        from .docx_parser import parse_docx
        return parse_docx
    elif file_type in ['application/pdf', '.pdf']:
        from .pdf_parser import parse_pdf
        return parse_pdf
    elif file_type in ['image/png', 'image/jpeg', 'image/jpg', '.png', '.jpg', '.jpeg']:
        from .image_parser import parse_image
        return parse_image
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
