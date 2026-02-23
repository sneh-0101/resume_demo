import spacy
import re

# Load spaCy model with fallback
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Common technical skills list (extendable)
SKILLS_DB = {
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "react", "angular", "vue",
    "sql", "mysql", "postgresql", "mongodb", "aws", "azure", "gcp", "docker", "kubernetes", "git",
    "flask", "django", "fastapi", "spring", "spring boot", "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "tableau", "power bi", "excel",
    "communication", "teamwork", "leadership", "agile", "scrum", "linux", "bash", "shell scripting"
}

def clean_text(text):
    """
    Basic text cleaning: remove special chars, extra spaces, lowercasing.
    """
    if not text:
        return ""
    text = text.lower()
    # Remove special characters but keep some useful for skills like c++, c#
    # We will replace newlines with space
    text = text.replace("\n", " ")
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    """
    Tokenization and lemmatization using spaCy.
    Returns a clean string of joined tokens.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def extract_skills(text):
    """
    Extracts skills from text based on the SKILLS_DB.
    This is a keyword-based matching approach for simplicity and speed.
    """
    found_skills = set()
    # We check for phrases in SKILLS_DB.
    # A simple token-based check might miss multi-word skills like "machine learning".
    # So we iterate over the skills db and check presence.
    # Note: This is O(N*M) where N is text length and M is num skills. 
    # For a resume and ~100 skills, it's fast enough.
    
    # Normalize text for matching
    text_lower = text.lower()
    
    # Using regex to match whole words/phrases to avoid partial matches (e.g. "java" in "javascript")
    # Escaping special chars for regex (like c++, c#)
    for skill in SKILLS_DB:
        # Create a regex pattern for the skill
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return sorted(list(found_skills))

def generate_suggestions(missing_skills):
    """
    Generates actionable suggestions based on missing skills.
    """
    suggestions = []
    if not missing_skills:
        return ["Great job! Your profile matches the required technical skills well."]
    
    for skill in missing_skills:
        suggestions.append(f"Consider adding a project or certification involving **{skill.title()}** to your portfolio.")
    
    suggestions.append("Ensure your resume highlights quantifiable achievements (e.g., 'Improved efficiency by 20%').")
    return suggestions

def generate_critique(missing_skills, score, resume_text):
    """
    Generates a detailed, point-wise critique of the resume.
    """
    critique = []
    
    # 1. Score Analysis
    if score >= 80:
        critique.append("🌟 **Overall**: Excellent profile! Your resume is highly relevant to the job description.")
    elif score >= 50:
        critique.append("⚠️ **Overall**: Good potential, but there are some critical keywords missing.")
    else:
        critique.append("❌ **Overall**: Your resume needs significant alignment with the job description.")
        
    # 2. Content Length Check
    word_count = len(resume_text.split())
    if word_count < 200:
        critique.append("📉 **Length**: Your resume seems a bit short. Elaborate on your experiences to add depth.")
    elif word_count > 1000:
        critique.append("📈 **Length**: Your resume is quite long. Try to keep it concise and focused on relevant experiences.")
    else:
        critique.append("✅ **Length**: Your resume length is optimal.")
        
    # 3. Missing Skills Impact
    if len(missing_skills) > 5:
        critique.append(f"🛠️ **Skills Gap**: You are missing {len(missing_skills)} key skills. Prioritize adding high-impact keywords like **{missing_skills[0].title()}** and **{missing_skills[1].title()}**.")
    elif missing_skills:
        critique.append(f"🔧 **Refinement**: You are close! Adding **{missing_skills[0].title()}** would strengthen your profile.")
    else:
        critique.append("🎉 **Skills**: Your technical skillset is a perfect match!")
        
    # 4. Action Verbs Check (Simple Heuristic)
    action_verbs = ["led", "developed", "built", "managed", "created", "designed", "implemented", "optimized"]
    found_verbs = [verb for verb in action_verbs if verb in resume_text.lower()]
    if len(found_verbs) < 3:
        critique.append("⚡ **Impact**: Use more strong action verbs (e.g., Led, Developed, Optimized) to describe your achievements.")
    else:
        critique.append("💪 **Impact**: Good use of action verbs to describe your contributions.")
        
    return critique

