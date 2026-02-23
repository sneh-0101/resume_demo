"""
PDF Resume Parser
Extracts text from PDF resume files
"""

import pdfplumber


class ResumeParser:
    """
    Parses PDF resume files and extracts text content
    """
    
    @staticmethod
    def extract_text(file_path):
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
        
        Returns:
            Extracted text content or empty string if parsing fails
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                # Extract text from all pages
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            return ""
