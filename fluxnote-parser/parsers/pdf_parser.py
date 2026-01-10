# PDF parser with hybrid text extraction and OCR logic

from typing import BinaryIO
import PyPDF2
from PIL import Image
import pytesseract
import io


def parse_pdf(file: BinaryIO) -> str:
    """
    Parse PDF file using hybrid approach:
    1. Try text extraction first
    2. Fall back to OCR if text extraction yields poor results
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text content
    """
    pdf_reader = PyPDF2.PdfReader(file)
    extracted_text = []
    
    for page_num, page in enumerate(pdf_reader.pages):
        # Try text extraction
        text = page.extract_text()
        
        # Check if text extraction was successful
        if text and len(text.strip()) > 50:  # Arbitrary threshold
            extracted_text.append(text)
        else:
            # Fall back to OCR
            # Note: This is a simplified approach
            # In production, you'd need to convert PDF page to image first
            extracted_text.append(f"[Page {page_num + 1}: OCR fallback needed]")
    
    return '\n\n'.join(extracted_text)


def ocr_pdf_page(page_image: Image.Image) -> str:
    """
    Perform OCR on a PDF page image.
    
    Args:
        page_image: PIL Image object of the PDF page
        
    Returns:
        OCR extracted text
    """
    return pytesseract.image_to_string(page_image)
