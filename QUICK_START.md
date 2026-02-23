# Quick Start Guide - Flask Application

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements_flask.txt
python -m spacy download en_core_web_sm
```

### Step 2: Run the Application
```bash
python run.py
```

The application will start at `http://localhost:5000`

### Step 3: Create an Account
1. Click "Register" in the navigation bar
2. Fill in your details
3. Click "Register"

### Step 4: Upload Resume
1. Go to "Upload Resume"
2. Select a PDF file
3. Click "Upload Resume"

### Step 5: Analyze
1. Go to "My Resumes"
2. Click "Analyze" on your resume
3. Paste a job description
4. Click "Analyze Now"
5. View your results and download the PDF report

## 📁 Project Structure

```
flask_app/
├── ai_engine/           # AI/ML logic (UNCHANGED from original)
│   └── core.py         # All AI functionality
├── routes/             # Flask routing (NEW)
│   ├── auth.py        # Authentication
│   ├── main.py        # Main pages
│   ├── dashboard.py   # Dashboard
│   └── analysis.py    # Core analysis features
├── templates/          # HTML templates (NEW)
├── models.py          # Database models (NEW)
├── forms.py           # Form validation (NEW)
└── config.py          # Configuration (NEW)

uploads/               # User uploads directory
```

## 🔑 Key Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/auth/register` | GET/POST | User registration |
| `/auth/login` | GET/POST | User login |
| `/dashboard` | GET | User dashboard |
| `/analysis/upload` | GET/POST | Upload resume |
| `/analysis/resumes` | GET | List resumes |
| `/analysis/resume/<id>/analyze` | GET/POST | Analyze resume |
| `/analysis/result/<id>` | GET | View results |
| `/analysis/result/<id>/report` | GET | Download PDF report |
| `/analysis/quick-analysis` | GET/POST | Demo analysis (no login) |

## 🧠 AI Engine Usage

All AI functionality is in `flask_app/ai_engine/core.py`:

```python
from flask_app.ai_engine import (
    ResumeParser,
    NLPProcessor,
    ResumeMatcher,
    ReportGenerator
)

# Extract text from PDF
text = ResumeParser.extract_text_from_pdf(pdf_file)

# Extract skills
skills = NLPProcessor.extract_skills(text)

# Calculate match score
score = ResumeMatcher.calculate_hybrid_score(
    resume_text, jd_text, resume_skills, jd_skills
)

# Generate report
report = ReportGenerator.generate_report(
    name, score, matched, missing, suggestions
)
```

## 🗄️ Database Models

### User
- Stores user accounts and authentication
- Links to resumes and analyses

### Resume
- Stores uploaded PDFs and extracted data
- Links to analyses

### Analysis
- Stores match results
- Tracks scores and suggestions

### JobPosting (Optional)
- For future job board integration

## 📊 Matching Algorithm

```
Score = (0.4 × TF-IDF Similarity) + (0.6 × Skill Match Rate)
```

- **TF-IDF**: Content similarity using sklearn
- **Skill Match**: Detected skills vs job requirements
- **Scale**: 0-100%

## 🔐 Security

✅ Password hashing (Werkzeug)
✅ CSRF protection (Flask-WTF)
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Secure file uploads (type & size validation)
✅ Session management (Flask-Login)

## 🎨 UI Features

- Dark mode support (CSS variables)
- Bootstrap 5.3 responsive design
- Font Awesome icons
- Smooth animations
- Mobile-friendly

## 📝 Forms

| Form | Fields | Purpose |
|------|--------|---------|
| RegistrationForm | username, email, password, name | Create account |
| LoginForm | email, password | User login |
| ResumeUploadForm | resume_file | Upload PDF |
| JobMatchingForm | job_description | Analyze match |
| QuickAnalysisForm | resume_file, job_description | Quick demo |

## 🛠️ Configuration

```python
# Development
FLASK_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///app.db

# Production
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://...
SECRET_KEY=secure-key-here
```

## 📦 Dependencies

### Core
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Flask-WTF 1.2.1

### AI/ML
- spaCy 3.7.2
- scikit-learn 1.3.2
- pdfplumber 10.3

### Frontend
- Bootstrap 5.3 (CDN)
- Font Awesome 6.4 (CDN)

## 🚨 Common Issues

**spaCy model missing:**
```bash
python -m spacy download en_core_web_sm
```

**Port already in use:**
```bash
flask run --port 5001
```

**Database error:**
```bash
rm instance/app.db
python -c "from flask_app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## 📚 Documentation

- Full documentation: `FLASK_README.md`
- Original Streamlit app: `app.py` (kept for reference)
- AI logic: `flask_app/ai_engine/core.py`

## 🎯 Next Steps

1. ✅ Run the application
2. ✅ Create an account
3. ✅ Upload a resume (PDF)
4. ✅ Analyze against a job description
5. ✅ Download the PDF report

Enjoy your Flask resume analyzer! 🚀
