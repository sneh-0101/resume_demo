import os
import sys
import time
from reportlab.pdfgen import canvas

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.parser as parser
import utils.nlp_processing as nlp_processing
import utils.matcher as matcher

def create_dummy_resume(filename="test_resume.pdf"):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 730, "Software Engineer")
    c.drawString(100, 700, "Skills: Python, Java, Machine Learning, SQL, Git.")
    c.drawString(100, 680, "Experience: Worked on AWS and Docker.")
    c.save()
    return filename

def test_pipeline():
    print("Starting Pipeline Verification...")
    start_time = time.time()
    
    # 1. Create PDF
    pdf_path = create_dummy_resume()
    print(f"Created dummy PDF: {pdf_path}")
    
    # 2. Extract Text
    with open(pdf_path, "rb") as f:
        text = parser.extract_text_from_pdf(f)
    print(f"Extracted Text: {text.strip()}")
    assert "John Doe" in text
    assert "Python" in text
    
    # 3. Process & Match
    jd_text = "We are looking for a Software Engineer with Python, Machine Learning, and SQL skills. Experience with AWS is a plus. Must know Docker."
    
    resume_clean = nlp_processing.clean_text(text)
    jd_clean = nlp_processing.clean_text(jd_text)
    
    resume_lemma = nlp_processing.preprocess_text(resume_clean)
    jd_lemma = nlp_processing.preprocess_text(jd_clean)
    
    score = matcher.calculate_match_score(resume_lemma, jd_lemma)
    print(f"Match Score: {score}%")
    
    # 4. Skills
    resume_skills = nlp_processing.extract_skills(resume_clean)
    jd_skills = nlp_processing.extract_skills(jd_clean)
    
    print(f"Resume Skills: {resume_skills}")
    print(f"JD Skills: {jd_skills}")
    
    matched = set(resume_skills).intersection(set(jd_skills))
    missing = set(jd_skills).difference(set(resume_skills))
    
    print(f"Matched: {matched}")
    print(f"Missing: {missing}")
    
    # Assertions
    assert "python" in resume_skills
    assert "docker" in resume_skills
    assert score > 50  # Should be a decent match
    assert len(matched) >= 3
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"Total Execution Time: {duration:.2f} seconds")
    
    if duration < 5:
        print("Performance check PASSED (< 5s)")
    else:
        print("Performance check FAILED (> 5s)")
        
    # Cleanup
    try:
        os.remove(pdf_path)
    except:
        pass

if __name__ == "__main__":
    try:
        test_pipeline()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
