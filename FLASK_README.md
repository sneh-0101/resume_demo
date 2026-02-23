# AI Resume Analyzer - Flask Web Application

A production-ready Flask web application for AI-powered resume analysis and job matching using NLP and machine learning.

## Features

✨ **Smart Resume Parsing**
- Advanced PDF extraction and text processing
- Automatic skill detection using machine learning
- Resume storage and version management

🎯 **Precision Job Matching**
- Hybrid TF-IDF + Skill-based matching algorithm
- Match score calculation (40% content similarity + 60% skill match)
- Comprehensive skill gap analysis

💡 **Actionable Insights**
- Detailed matched/missing skills breakdown
- AI-generated improvement suggestions
- Professional PDF report generation
- Analysis history tracking

👤 **User Management**
- Secure user registration and authentication
- Password hashing with Werkzeug
- Persistent user sessions
- Personal dashboard with analytics

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy (supports SQLite, PostgreSQL, MySQL)
- **Authentication**: Flask-Login
- **Forms**: WTForms with CSRF protection

### AI/ML
- **NLP**: spaCy (en_core_web_sm)
- **Text Analysis**: scikit-learn TF-IDF Vectorizer
- **PDF Processing**: pdfplumber
- **Report Generation**: reportlab

### Frontend
- **HTML/Templates**: Jinja2
- **CSS Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **JavaScript**: Vanilla JS with Bootstrap utilities

## Project Structure

```
flask_app/
├── ai_engine/              # AI/ML modules
│   ├── __init__.py
│   └── core.py            # ResumeParser, NLPProcessor, ResumeMatcher, ReportGenerator
├── routes/                # Flask blueprints (MVC controllers)
│   ├── auth.py           # Login/Register
│   ├── main.py           # Home, Dashboard, About
│   ├── dashboard.py      # User dashboard
│   └── analysis.py       # Resume upload and analysis
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── dashboard/
│   └── analysis/
├── static/               # CSS, JS, images
│   ├── css/style.css
│   └── js/main.js
├── models.py            # SQLAlchemy ORM models
├── forms.py             # WTForms validation
├── utils.py             # Utility functions
├── config.py            # Configuration (Dev, Test, Prod)
└── __init__.py          # Flask app factory

uploads/                 # User resume uploads (auto-created)
instance/               # Instance folder for database
run.py                  # Application entry point
```

## Installation & Setup

### 1. Clone Repository
```bash
cd d:\AI-Driven-Resume-Analyzer-with-Automated-Job-Matching
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements_flask.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 4. Set Environment Variables
```bash
# On Windows
set FLASK_APP=run.py
set FLASK_ENV=development
set SECRET_KEY=your-secret-key-here

# On Linux/Mac
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here
```

### 5. Initialize Database
```bash
# Using Flask shell
flask shell
>>> from flask_app import db
>>> db.create_all()
>>> exit()
```

### 6. Run Development Server
```bash
python run.py
# or
flask run
```

Visit `http://localhost:5000` in your browser.

## API Routes

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/register` - Registration page
- `POST /auth/register` - Create account
- `GET /auth/logout` - Logout

### Main Pages
- `GET /` - Home page
- `GET /dashboard` - User dashboard
- `GET /features` - Features page
- `GET /about` - About page

### Resume Management
- `GET /analysis/upload` - Upload resume form
- `POST /analysis/upload` - Process upload
- `GET /analysis/resumes` - List user resumes
- `POST /analysis/resume/<id>/delete` - Delete resume

### Analysis
- `GET /analysis/quick-analysis` - Quick demo analysis
- `POST /analysis/quick-analysis` - Process quick analysis
- `GET /analysis/resume/<id>/analyze` - Analysis form for specific resume
- `POST /analysis/resume/<id>/analyze` - Process analysis
- `GET /analysis/result/<id>` - View analysis results
- `GET /analysis/result/<id>/report` - Download PDF report
- `GET /analysis/history` - View all analyses

## Configuration

### Development Config
```python
# flask_app/config.py
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SESSION_COOKIE_SECURE = False
```

### Production Config
```python
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
```

## Database Models

### User
- id, username, email, password_hash
- first_name, last_name
- created_at, updated_at
- Relationships: resumes, analyses

### Resume
- id, user_id, filename, filepath
- extracted_text, extracted_skills
- created_at, updated_at
- Relationships: user, analyses

### Analysis
- id, user_id, resume_id, job_id
- match_score, matched_skills, missing_skills
- suggestions, match_percentage
- job_description
- created_at, updated_at
- Relationships: user, resume, job

### JobPosting
- id, title, company, description
- required_skills, salary_min, salary_max
- location, job_url
- created_at, updated_at
- Relationships: analyses

## Core AI Engine Classes

### ResumeParser
```python
from flask_app.ai_engine import ResumeParser

# Extract text from PDF
text = ResumeParser.extract_text_from_pdf(file)
```

### NLPProcessor
```python
from flask_app.ai_engine import NLPProcessor

# Extract skills from text
skills = NLPProcessor.extract_skills(text)

# Generate suggestions
suggestions = NLPProcessor.generate_suggestions(missing_skills)

# Preprocess text
processed = NLPProcessor.preprocess_text(text)
```

### ResumeMatcher
```python
from flask_app.ai_engine import ResumeMatcher

# Calculate match score
score = ResumeMatcher.calculate_hybrid_score(
    resume_text, jd_text, resume_skills, jd_skills
)

# Perform full analysis
analysis = ResumeMatcher.analyze_match(
    resume_text, jd_text, resume_skills, jd_skills
)
```

### ReportGenerator
```python
from flask_app.ai_engine import ReportGenerator

# Generate PDF report
report_buffer = ReportGenerator.generate_report(
    resume_name, score, matched_skills, 
    missing_skills, suggestions
)
```

## Usage Examples

### Upload and Analyze Resume
```python
# 1. User uploads resume (handled by forms.py)
# 2. Extract text
text = ResumeParser.extract_text_from_pdf(uploaded_file)

# 3. Extract skills
skills = NLPProcessor.extract_skills(text)

# 4. Store in database
resume = Resume(
    user_id=user_id,
    filename=filename,
    filepath=filepath,
    extracted_text=text,
    extracted_skills=skills
)
db.session.add(resume)
db.session.commit()

# 5. Analyze against job description
jd_skills = NLPProcessor.extract_skills(jd_text)
analysis = ResumeMatcher.analyze_match(text, jd_text, skills, jd_skills)

# 6. Generate report
report = ReportGenerator.generate_report(
    filename, analysis['score'],
    analysis['matched_skills'],
    analysis['missing_skills'],
    suggestions
)
```

## File Upload Handling

- **Location**: `uploads/` directory (auto-created)
- **Organization**: `uploads/<user_id>/<unique_filename>`
- **Max Size**: 16MB
- **Allowed Types**: PDF only
- **Security**: Unique naming with UUID to prevent collisions

## Matching Algorithm

```
Final Score = (40% × TF-IDF Similarity) + (60% × Skill Match Ratio)

TF-IDF Similarity:
  - Vectorizes resume and job description
  - Calculates cosine similarity
  - Measures content overlap

Skill Match Ratio:
  - Counts matching skills
  - Ratio = matched_skills / total_required_skills
  - More weight on skills for technical roles
```

## Security Features

✅ **Password Security**
- Werkzeug password hashing (PBKDF2)
- Salt-based storage

✅ **Session Management**
- Flask-Login with remember-me functionality
- Secure session cookies (HTTPOnly, SameSite)

✅ **Form Security**
- CSRF protection with Flask-WTF
- Input validation with WTForms

✅ **File Upload Security**
- File type validation (PDF only)
- File size limits (16MB)
- Unique filename generation (UUID)

✅ **Database Security**
- SQL injection prevention via SQLAlchemy ORM
- Parameterized queries

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements_flask.txt .
RUN pip install -r requirements_flask.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Environment Variables for Production
```
FLASK_ENV=production
SECRET_KEY=your-secure-random-key
DATABASE_URL=postgresql://user:pass@localhost/db
UPLOAD_FOLDER=/var/uploads
```

## Performance Optimization

- Database indexing on frequently queried fields
- Lazy loading for relationships
- Query optimization with select_related/joined_load
- Caching layer ready for Redis integration
- Static file compression (CSS/JS minification recommended)

## Logging & Monitoring

```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Future Enhancements

🔮 Planned Features:
- LinkedIn profile integration
- Job board API integration (Indeed, LinkedIn, etc.)
- Batch resume analysis
- Team/organizational accounts
- Advanced analytics dashboard
- Email notifications
- Resume optimization suggestions
- Interview question generation
- Salary insights

## Troubleshooting

**Issue**: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

**Issue**: Database locked
```bash
# Remove existing database
rm instance/app.db
# Reinitialize
flask shell
>>> from flask_app import db
>>> db.create_all()
```

**Issue**: Port already in use
```bash
# Use different port
flask run --port 5001
```

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Version

- **Flask Application**: 1.0.0
- **AI Engine**: 1.0.0
- **Last Updated**: January 2026
