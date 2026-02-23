import os
import sys
import time
from reportlab.pdfgen import canvas

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.parser as parser
import utils.nlp_processing as nlp_processing
import utils.matcher as matcher
import utils.report_generator as report_generator

def create_dummy_resume(filename="test_resume_v2.pdf"):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Jane Doe")
    c.drawString(100, 730, "Data Scientist")
    c.drawString(100, 700, "Skills: Python, SQL, Tableau, Pandas, NumPy.")
    c.drawString(100, 680, "Experience: Built predictive models.")
    c.save()
    return filename

def test_enhanced_flow():
    print("Starting Enhanced Verification...")
    
    # 1. Create PDF
    pdf_path = create_dummy_resume()
    
    # 2. Extract Text
    with open(pdf_path, "rb") as f:
        text = parser.extract_text_from_pdf(f)
    
    # 3. Match Logic
    jd_text = "Looking for a Data Scientist with Python, SQL, Pandas, and AWS skills."
    
    resume_clean = nlp_processing.clean_text(text)
    jd_clean = nlp_processing.clean_text(jd_text)
    
    resume_lemma = nlp_processing.preprocess_text(resume_clean)
    jd_lemma = nlp_processing.preprocess_text(jd_clean)
    
    resume_skills = nlp_processing.extract_skills(resume_clean)
    jd_skills = nlp_processing.extract_skills(jd_clean)
    
    # Test Hybrid Score
    score = matcher.calculate_hybrid_score(resume_lemma, jd_lemma, resume_skills, jd_skills)
    print(f"Hybrid Score: {score}%")
    assert score > 0
    
    # Test Suggestions
    matched = sorted(list(set(resume_skills).intersection(set(jd_skills))))
    missing = sorted(list(set(jd_skills).difference(set(resume_skills))))
    
    suggestions = nlp_processing.generate_suggestions(missing)
    print("Suggestions Generated:", suggestions)
    assert len(suggestions) > 0
    # Check for AWS (title case might be Aws or AWS depending on python version/logic)
    # Suggestions text: "... involving **Aws** ..."
    assert "aws" in str(suggestions).lower() # Case insensitive check
    
    # Test Report Generation
    print("Generating Report...")
    pdf_bytes = report_generator.generate_report("Jane Doe", score, matched, missing, suggestions)
    assert len(pdf_bytes.getvalue()) > 0
    print("Report generated successfully.")

    # Cleanup
    try:
        os.remove(pdf_path)
    except:
        pass

if __name__ == "__main__":
    try:
        test_enhanced_flow()
        print("ALL ENHANCED TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
