"""
AI Engine - Unified interface for all AI/ML operations
Organizes existing AI logic: resume parsing, NLP processing, and matching
"""

import pdfplumber
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io


class ResumeParser:
    """Handles resume parsing from PDF files"""
    
    @staticmethod
    def extract_text_from_pdf(file):
        """
        Extracts text from a PDF file object.
        
        Args:
            file: File object (like werkzeug.datastructures.FileStorage)
        
        Returns:
            str: Extracted text or None if error
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


class NLPProcessor:
    """Handles NLP processing and skill extraction"""
    
    # Load spaCy model with fallback
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading 'en_core_web_sm' model...")
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    # Common technical skills database (extendable)
    SKILLS_DB = {
        "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "react", "angular", "vue",
        "sql", "mysql", "postgresql", "mongodb", "aws", "azure", "gcp", "docker", "kubernetes", "git",
        "flask", "django", "fastapi", "spring", "spring boot", "machine learning", "deep learning", "nlp",
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "tableau", "power bi", "excel",
        "communication", "teamwork", "leadership", "agile", "scrum", "linux", "bash", "shell scripting",
        "rest api", "graphql", "microservices", "ci/cd", "jenkins", "gitlab", "github", "jira"
    }
    
    @classmethod
    def clean_text(cls, text):
        """
        Basic text cleaning: remove special chars, extra spaces, lowercasing.
        
        Args:
            text: Raw text string
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        text = text.lower()
        text = text.replace("\n", " ")
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @classmethod
    def preprocess_text(cls, text):
        """
        Tokenization and lemmatization using spaCy.
        
        Args:
            text: Raw text string
            
        Returns:
            str: Preprocessed text with lemmatized tokens
        """
        doc = cls.nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(tokens)
    
    @classmethod
    def extract_skills(cls, text):
        """
        Extracts skills from text based on the SKILLS_DB.
        Uses keyword-based matching with regex for word boundaries.
        
        Args:
            text: Input text
            
        Returns:
            list: Sorted list of found skills
        """
        found_skills = set()
        text_lower = text.lower()
        
        for skill in cls.SKILLS_DB:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    @classmethod
    def check_ats_friendliness(cls, text):
        """
        Checks for ATS friendliness: sections, contact info, formatting.
        
        Returns:
            dict: ATS score and detailed findings
        """
        if not text:
            return {'score': 0, 'details': {'error': 'No text provided'}}
            
        text_lower = text.lower()
        findings = []
        score = 0
        
        # 1. Section Checks (30 points)
        sections = {
            'experience': ['experience', 'work history', 'employment'],
            'education': ['education', 'academic'],
            'skills': ['skills', 'technologies', 'expertise'],
            'summary': ['summary', 'objective', 'profile'],
            'contact': ['contact', 'personal info']
        }
        
        section_score = 0
        for section, keywords in sections.items():
            if any(k in text_lower for k in keywords):
                section_score += 6
            else:
                findings.append(f"Missing '{section.title()}' section header.")
        score += section_score
        
        # 2. Contact Info (20 points)
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        
        if re.search(email_pattern, text):
            score += 10
        else:
            findings.append("Email address not detected.")
            
        if re.search(phone_pattern, text):
            score += 10
        else:
            findings.append("Phone number not detected.")
            
        # 3. Text Volume/Density (20 points)
        word_count = len(text.split())
        if 200 <= word_count <= 1000:
            score += 20
        elif word_count < 200:
            score += 10
            findings.append("Resume text is quite short; consider adding more detail.")
        else:
            score += 15
            findings.append("Resume is very long; ensure it remains concise.")
            
        # 4. Formatting - No tables/columns detection (simulated) (30 points)
        # In a real app, we'd check PDF structure. Here we check for common clean text patterns.
        # We'll grant 30 points if it passes basic "sanity" of not having too many weird chars
        special_chars = len(re.findall(r'[^\w\s,.()-]', text))
        if special_chars / max(word_count, 1) < 0.05:
            score += 30
        else:
            score += 15
            findings.append("Detected high density of special characters; check for complex formatting.")
            
        return {
            'score': score,
            'findings': findings
        }

    @classmethod
    def generate_suggestions(cls, missing_skills):
        """
        Generates actionable improvement suggestions.
        
        Args:
            missing_skills: List of missing skills
            
        Returns:
            list: Suggestions for improvement
        """
        suggestions = []
        if not missing_skills:
            return ["Great job! Your profile matches the required technical skills well."]
        
        for skill in missing_skills:
            suggestions.append(f"Consider adding a project or certification involving {skill.title()} to your portfolio.")
        
        return suggestions


class InterviewPrep:
    """Generates interview questions based on missing skills"""
    
    # Simple question bank mapping (can be expanded or replaced with LLM)
    QUESTION_BANK = {
        "python": [
            "Explain the difference between list and tuple.",
            "What represent decorators and how are they used?",
            "How does memory management work in Python?"
        ],
        "java": [
            "What is the difference between JDK, JRE, and JVM?",
            "Explain the concept of OOPs.",
            "What is the difference between an checks and unchecked exception?"
        ],
        "javascript": [
            "Explain closures in JavaScript.",
            "What is the difference between `==` and `===`?",
            "Explain the event loop."
        ],
        "sql": [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "Explain ACID properties.",
            "How do you optimize a slow query?"
        ],
        "react": [
            "What are hooks and why do we use them?",
            "Explain the Virtual DOM.",
            "What is the difference between state and props?"
        ],
        "docker": [
            "What is the difference between an image and a container?",
            "Explain the Dockerfile instructions.",
            "How do you manage data in Docker?"
        ],
        "aws": [
            "What is the difference between S3 and EBS?",
            "Explain the concept of VPC.",
            "What is a Lambda function?"
        ],
        "machine learning": [
            "What is the difference between supervised and unsupervised learning?",
            "Explain the bias-variance tradeoff.",
            "How do you handle overfitting?"
        ]
    }
    
    @classmethod
    def generate_questions(cls, missing_skills):
        """
        Generates interview questions for missing skills.
        
        Args:
            missing_skills: List of missing skills
            
        Returns:
            list: List of questions
        """
        questions = []
        for skill in missing_skills:
            skill_lower = skill.lower()
            if skill_lower in cls.QUESTION_BANK:
                questions.extend(cls.QUESTION_BANK[skill_lower][:2]) # Get top 2 questions
            else:
                # Generic question if skill not in bank
                questions.append(f"Can you describe your experience with {skill}?")
                questions.append(f"What was the most challenging project you built using {skill}?")
                
        return questions[:10] # Limit to 10 questions max


class SkillRecommender:
    """Provides learning resources for skills"""
    
    RESOURCE_MAP = {
        "python": {"name": "Python 3 Docs", "url": "https://docs.python.org/3/"},
        "java": {"name": "Oracle Java Tutorials", "url": "https://docs.oracle.com/javase/tutorial/"},
        "javascript": {"name": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"},
        "react": {"name": "React Official Docs", "url": "https://react.dev/"},
        "sql": {"name": "W3Schools SQL", "url": "https://www.w3schools.com/sql/"},
        "docker": {"name": "Docker Get Started", "url": "https://www.docker.com/get-started/"},
        "aws": {"name": "AWS Training", "url": "https://aws.amazon.com/training/"},
        "machine learning": {"name": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"}
    }
    
    @classmethod
    def get_resources(cls, missing_skills):
        """
        Get learning resources for missing skills.
        
        Args:
            missing_skills: List of skills
            
        Returns:
            list: List of dicts {skill, name, url}
        """
        resources = []
        for skill in missing_skills:
            skill_lower = skill.lower()
            if skill_lower in cls.RESOURCE_MAP:
                res = cls.RESOURCE_MAP[skill_lower]
                resources.append({
                    "skill": skill,
                    "name": res["name"],
                    "url": res["url"]
                })
            else:
                # Generic search link
                resources.append({
                    "skill": skill,
                    "name": f"Search '{skill}' on Coursera",
                    "url": f"https://www.coursera.org/search?query={skill}"
                })
        return resources


class ResumeMatcher:
    """Handles resume to job description matching"""
    
    @staticmethod
    def calculate_tfidf_score(resume_text, jd_text):
        """
        Calculates the cosine similarity between resume and job description using TF-IDF.
        
        Args:
            resume_text: Resume content
            jd_text: Job description content
            
        Returns:
            float: Similarity score between 0 and 1
        """
        if not resume_text or not jd_text:
            return 0.0
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity
    
    @staticmethod
    def calculate_hybrid_score(resume_text, jd_text, resume_skills, jd_skills):
        """
        Calculates a weighted hybrid score based on TF-IDF and skill matching.
        Weight: 40% Content Similarity + 60% Skill Match (better for technical roles)
        
        Args:
            resume_text: Resume content
            jd_text: Job description content
            resume_skills: List of skills found in resume
            jd_skills: List of skills required in job description
            
        Returns:
            float: Final score between 0 and 100
        """
        if not resume_text or not jd_text:
            return 0.0
        
        # Content similarity using TF-IDF
        content_sim = ResumeMatcher.calculate_tfidf_score(resume_text, jd_text)
        
        # Skill match ratio
        if not jd_skills:
            skill_match = 1.0 if resume_skills else 0.0
        else:
            matched_count = len(set(resume_skills).intersection(set(jd_skills)))
            skill_match = matched_count / len(jd_skills)
        
        # Weighted average: 40% TF-IDF + 60% Skills
        final_score = (content_sim * 0.4) + (skill_match * 0.6)
        
        return round(final_score * 100, 2)
    
    @staticmethod
    def analyze_match(resume_text, jd_text, resume_skills, jd_skills):
        """
        Performs comprehensive match analysis.
        
        Returns:
            dict: Analysis results including score, matched/missing skills, ATS data,
                  interview questions, and skill resources.
        """
        score = ResumeMatcher.calculate_hybrid_score(resume_text, jd_text, resume_skills, jd_skills)
        ats_data = NLPProcessor.check_ats_friendliness(resume_text)
        
        matched_skills = list(set(resume_skills) & set(jd_skills))
        missing_skills = list(set(jd_skills) - set(resume_skills))
        missing_skills.sort()
        
        # New Feature Integration
        interview_questions = InterviewPrep.generate_questions(missing_skills)
        skill_resources = SkillRecommender.get_resources(missing_skills)
        
        return {
            'score': score,
            'matched_skills': sorted(matched_skills),
            'missing_skills': missing_skills,
            'match_percentage': min(100, int((len(matched_skills) / max(len(jd_skills), 1)) * 100)),
            'ats_score': ats_data['score'],
            'ats_findings': ats_data['findings'],
            'interview_questions': interview_questions,
            'skill_resources': skill_resources
        }


class ReportGenerator:
    """Generates PDF reports for resume analysis"""
    
    @staticmethod
    def generate_report(resume_name, match_score, matched_skills, missing_skills, suggestions, ats_score=None, ats_findings=None):
        """
        Generates a professional PDF report for resume analysis.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            rightMargin=72, 
            leftMargin=72, 
            topMargin=72, 
            bottomMargin=18
        )
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Header', fontSize=18, spaceAfter=20, alignment=1, 
                                 textColor=colors.HexColor("#4F46E5")))
        styles.add(ParagraphStyle(name='SubSection', fontSize=14, spaceBefore=15, spaceAfter=10, 
                                 textColor=colors.HexColor("#4F46E5")))
        
        elements = []
        
        # Title
        elements.append(Paragraph("AI Resume Analysis Report", styles['Header']))
        elements.append(Paragraph(f"Candidate: {resume_name}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Scores Section
        col1_text = f"Match Score: <font color='#4F46E5'><b>{match_score}%</b></font>"
        elements.append(Paragraph(col1_text, styles['SubSection']))
        
        if ats_score is not None:
            ats_color = '#10B981' if ats_score >= 70 else '#F59E0B' if ats_score >= 40 else '#EF4444'
            elements.append(Paragraph(f"ATS Friendliness Score: <font color='{ats_color}'><b>{ats_score}%</b></font>", 
                                     styles['SubSection']))
        
        elements.append(Spacer(1, 12))
        
        # Skills table
        elements.append(Paragraph("Skill Analysis:", styles['SubSection']))
        
        data = [['Matched Skills', 'Missing Skills']]
        max_len = max(len(matched_skills), len(missing_skills))
        
        for i in range(max_len):
            m = matched_skills[i] if i < len(matched_skills) else ""
            miss = missing_skills[i] if i < len(missing_skills) else ""
            data.append([m, miss])
        
        if not data[1:]:
            data.append(["None", "None"])
        
        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F3F4F6")),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # ATS Findings
        if ats_findings:
            elements.append(Paragraph("ATS Friendliness Feedback:", styles['SubSection']))
            for finding in ats_findings:
                elements.append(Paragraph(f"• {finding}", styles['Normal']))
                elements.append(Spacer(1, 6))
            elements.append(Spacer(1, 12))
        
        # Suggestions
        elements.append(Paragraph("Improvement Suggestions:", styles['SubSection']))
        for suggestion in suggestions:
            elements.append(Paragraph(f"• {suggestion}", styles['Normal']))
            elements.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
