# Image parser using OCR

from typing import BinaryIO
from PIL import Image
import pytesseract


def parse_image(file: BinaryIO) -> str:
    """
    Parse image file using OCR (Optical Character Recognition).
    
    Args:
        file: Binary file object
        
    Returns:
        OCR extracted text content
    """
    # Open image
    image = Image.open(file)
    
    # Perform OCR
    text = pytesseract.image_to_string(image)
    
    return text
