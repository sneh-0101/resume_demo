import pdfplumber

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file object (like the one from Streamlit uploader).
    """
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text
