from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, jd_text):
    """
    Calculates the cosine similarity between the resume and job description.
    Returns a score between 0 and 100.
    """
    if not resume_text or not jd_text:
        return 0.0

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the documents
    # input must be a list of strings
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    
    # Calculate cosine similarity
    # tfidf_matrix[0] is resume, [1] is JD
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return similarity

def calculate_hybrid_score(resume_text, jd_text, resume_skills, jd_skills):
    """
    Calculates a weighted score based on TF-IDF similarity and Skill Match Ratio.
    Weight: 50% Content Similarity + 50% Skill Match
    """
    if not resume_text or not jd_text:
        return 0.0

    # 1. Content Similarity (TF-IDF)
    content_sim = calculate_match_score(resume_text, jd_text)
    
    # 2. Skill Match Ratio
    # Avoid division by zero
    if not jd_skills:
        skill_match = 1.0 if resume_skills else 0.0
    else:
        matched_count = len(set(resume_skills).intersection(set(jd_skills)))
        skill_match = matched_count / len(jd_skills)
    
    # Weighted Average
    # Adjust weights as needed. 0.4 TF-IDF + 0.6 Skills is usually better for tech jobs.
    final_score = (content_sim * 0.4) + (skill_match * 0.6)
    
    return round(final_score * 100, 2)
