"""
AI Resume Matching Engine
Uses TF-IDF and skill matching to calculate resume-to-job match scores
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


class SkillMatcher:
    """
    AI Engine for matching resumes to job postings
    Uses TF-IDF similarity and skill-based matching
    """
    
    # Common technical skills database
    SKILLS_DB = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby',
        'golang', 'rust', 'scala', 'kotlin', 'swift', 'objective-c',
        'html', 'css', 'react', 'vue', 'angular', 'svelte',
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'rails',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'jenkins',
        'git', 'linux', 'windows', 'macos',
        'api', 'rest', 'graphql', 'soap', 'grpc',
        'agile', 'scrum', 'kanban', 'devops',
        'machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch',
        'data analysis', 'data science', 'tableau', 'power bi',
        'communication', 'teamwork', 'leadership', 'problem solving'
    }
    
    @staticmethod
    def extract_skills(text):
        """
        Extract skills from text using regex pattern matching
        
        Args:
            text: Text to extract skills from (resume or job description)
        
        Returns:
            Set of extracted skills (lowercase)
        """
        if not text:
            return set()
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s\+\-\#\.]', ' ', text)
        
        # Find skills by pattern matching
        found_skills = set()
        
        for skill in SkillMatcher.SKILLS_DB:
            # Create pattern that matches whole words
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                found_skills.add(skill)
        
        return found_skills
    
    @staticmethod
    def calculate_tfidf_score(resume_text, job_description):
        """
        Calculate TF-IDF cosine similarity between resume and job description
        
        Args:
            resume_text: Full text of resume
            job_description: Full text of job description
        
        Returns:
            Similarity score (0-100)
        """
        if not resume_text or not job_description:
            return 0
        
        try:
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Return as percentage (0-100)
            return round(similarity * 100, 2)
        except:
            return 0
    
    @staticmethod
    def calculate_skill_match_score(resume_skills, job_skills):
        """
        Calculate skill match percentage
        
        Args:
            resume_skills: Set of skills from resume
            job_skills: Set of required skills from job
        
        Returns:
            Percentage of job skills found in resume
        """
        if not job_skills:
            return 100  # All skills satisfied if none required
        
        if not resume_skills:
            return 0  # No match if no skills in resume
        
        # Calculate intersection
        matched_skills = resume_skills.intersection(job_skills)
        skill_match_score = (len(matched_skills) / len(job_skills)) * 100
        
        return round(skill_match_score, 2)
    
    @staticmethod
    def analyze_match(resume_text, job_description, job_requirements=None):
        """
        Perform complete resume-to-job match analysis
        
        Args:
            resume_text: Full text from resume
            job_description: Full text of job description
            job_requirements: Optional additional requirements text
        
        Returns:
            Dictionary with match analysis:
            {
                'overall_score': float (0-100),
                'tfidf_score': float (0-100),
                'skill_score': float (0-100),
                'matched_skills': list,
                'missing_skills': list,
                'match_level': string (Poor/Fair/Good/Excellent)
            }
        """
        
        # Extract skills
        resume_skills = SkillMatcher.extract_skills(resume_text)
        
        # Combine job description and requirements for skill matching
        full_job_text = job_description
        if job_requirements:
            full_job_text += ' ' + job_requirements
        
        job_skills = SkillMatcher.extract_skills(full_job_text)
        
        # Calculate scores
        tfidf_score = SkillMatcher.calculate_tfidf_score(resume_text, job_description)
        skill_score = SkillMatcher.calculate_skill_match_score(resume_skills, job_skills)
        
        # Weighted overall score: 40% TF-IDF, 60% Skill Match
        overall_score = (tfidf_score * 0.4) + (skill_score * 0.6)
        
        # Determine match level
        if overall_score >= 80:
            match_level = 'Excellent'
        elif overall_score >= 60:
            match_level = 'Good'
        elif overall_score >= 40:
            match_level = 'Fair'
        else:
            match_level = 'Poor'
        
        # Get matched and missing skills
        matched = list(resume_skills.intersection(job_skills))
        missing = list(job_skills - resume_skills)
        
        return {
            'overall_score': round(overall_score, 2),
            'tfidf_score': tfidf_score,
            'skill_score': skill_score,
            'matched_skills': matched,
            'missing_skills': missing,
            'match_level': match_level,
            'resume_skills_count': len(resume_skills),
            'job_skills_count': len(job_skills)
        }
