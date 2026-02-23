# Flask Job Portal - Quick Navigation Index

## 🚀 Getting Started (5 minutes)

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python run.py`
3. **Open**: `http://localhost:5001`
4. **Register**: Create account as Job Seeker or Recruiter

---

## 📚 Documentation Files

### 📖 Main Documentation
- **[README.md](README.md)** - Complete feature overview and quick start
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup with code examples
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What was built and how to use it

### 🔗 Documentation Map

```
README.md               ← Start here! Feature overview
├── Quick Start         ← 5-minute setup
├── Project Structure   ← Folder organization
├── Features           ← What the app does
├── Tech Stack         ← Technologies used
└── Future Ideas       ← What could be added

SETUP_GUIDE.md          ← Detailed setup & examples
├── Installation        ← Step-by-step
├── Database Models     ← All 4 models
├── Feature Overview    ← How each feature works
├── API Endpoints       ← All 25+ routes
├── Code Examples       ← Copy-paste ready
└── Troubleshooting     ← Common issues

PROJECT_SUMMARY.md      ← Project completion
├── What Was Built      ← All components
├── Files Created       ← 25+ files
├── Key Features        ← User roles & AI
└── Next Steps          ← What to do now
```

---

## 💻 Key Application Files

### Entry Point
- **`run.py`** - Start here! Main application entry point

### Core Flask App
- **`app/__init__.py`** - Flask app factory, configuration
- **`app/config.py`** - Development, Testing, Production configs

### Database Layer
- **`app/models/__init__.py`** - 4 models: User, Job, Resume, Application

### Routing (Controllers)
- **`app/routes/auth.py`** - Login, register, logout
- **`app/routes/main.py`** - Home, dashboard redirect
- **`app/routes/job_seeker.py`** - Job seeker features (250+ lines)
- **`app/routes/recruiter.py`** - Recruiter features (180+ lines)
- **`app/routes/admin.py`** - Admin dashboard (130+ lines)

### AI Engine
- **`app/ai_engine/parser.py`** - PDF resume parsing
- **`app/ai_engine/matcher.py`** - AI matching algorithm (250+ lines)

### Frontend
- **`app/templates/`** - 15+ HTML templates
- **`app/static/style.css`** - Custom Bootstrap styling
- **`app/static/main.js`** - Client-side utilities

---

## 🎯 User Roles & Routes

### 1. **Job Seeker** 👤
Routes: `/seeker/*`
- Dashboard: View resumes, applications, stats
- Upload resume: PDF parsing with skill extraction
- Browse jobs: Search and filter job postings
- Apply: Submit applications with cover letter
- Track: View match scores and application status

**Key Files**:
- `app/routes/job_seeker.py` (250+ lines)
- `app/templates/job_seeker/` (5 templates)

### 2. **Recruiter** 🏢
Routes: `/recruiter/*`
- Dashboard: Posted jobs and applications overview
- Post job: Create new job listings
- Manage jobs: Edit and delete postings
- Review applications: See candidate profiles
- Track status: Update application progress

**Key Files**:
- `app/routes/recruiter.py` (180+ lines)
- `app/templates/recruiter/` (4 templates)

### 3. **Admin** 🔐
Routes: `/admin/*`
- Dashboard: Site-wide statistics
- Manage users: Activate/deactivate accounts
- Manage jobs: Review all postings
- Analytics: Application trends and reports

**Key Files**:
- `app/routes/admin.py` (130+ lines)
- `app/templates/admin/` (4 templates)

---

## 🤖 AI Matching Engine

**Location**: `app/ai_engine/matcher.py` (250+ lines)

### How It Works
1. Extract skills from resume using regex
2. Extract skills from job description
3. Calculate TF-IDF text similarity (40%)
4. Calculate skill match ratio (60%)
5. Return overall score + feedback

### Usage Example
```python
from app.ai_engine import SkillMatcher

result = SkillMatcher.analyze_match(
    resume_text="Python, AWS, Docker...",
    job_description="Senior Backend Engineer...",
    job_requirements="Python, AWS required"
)

print(f"Score: {result['overall_score']}%")  # 85.5
print(f"Matched: {result['matched_skills']}")  # ['python', 'aws']
print(f"Missing: {result['missing_skills']}")  # ['kubernetes']
```

### Skill Database
100+ technical and soft skills:
- Languages: Python, Java, JavaScript, C++, Go, Rust, etc.
- Frameworks: React, Vue, Django, Flask, Spring, Rails, etc.
- Databases: MySQL, MongoDB, PostgreSQL, Redis, etc.
- Cloud: AWS, Azure, GCP, Kubernetes, Docker, etc.
- Soft skills: Leadership, Communication, Teamwork, etc.

---

## 📊 Database Schema

### 4 Main Tables

```
┌─────────────────────┐
│      Users          │
├─────────────────────┤
│ id (PK)             │
│ username (UNIQUE)   │
│ email (UNIQUE)      │
│ password_hash       │
│ role (enum: 3)      │  ← 1 user, many roles
│ first_name          │
│ last_name           │
│ company             │
│ created_at          │
│ updated_at          │
└─────────────────────┘
         │ (recruiter)
         ├────────────────────┐
         │                    │
    ┌────▼──────────┐   ┌────▼──────────┐
    │   Jobs        │   │  Resumes      │
    ├───────────────┤   ├───────────────┤
    │ id (PK)       │   │ id (PK)       │
    │ title         │   │ filename      │
    │ description   │   │ filepath      │
    │ requirements  │   │ extracted_text│
    │ location      │   │ extracted_... │
    │ salary_*      │   │ user_id (FK)  │
    │ recruiter_id  │   │ created_at    │
    │ (FK) User     │   │ updated_at    │
    └────┬──────────┘   └───────┬───────┘
         │                      │
         └──────────┬───────────┘
                    │
            ┌───────▼─────────┐
            │  Applications   │
            ├─────────────────┤
            │ id (PK)         │
            │ job_id (FK)     │
            │ user_id (FK)    │
            │ resume_id (FK)  │
            │ status (enum)   │
            │ match_score     │
            │ matched_skills  │
            │ missing_skills  │
            │ applied_at      │
            │ updated_at      │
            └─────────────────┘
```

---

## 🛣️ All Routes (25+)

### Authentication Routes
```
GET  /auth/register           - Register page
POST /auth/register           - Create account
GET  /auth/login              - Login page
POST /auth/login              - Authenticate
GET  /auth/logout             - Logout
```

### Main Routes
```
GET /                         - Home page
GET /dashboard                - Role redirect
GET /jobs                     - Browse jobs
GET /job/<id>                 - Job details
```

### Job Seeker Routes (`/seeker/*`)
```
GET  /dashboard               - Dashboard
GET  /resume/upload           - Upload page
POST /resume/upload           - Save resume
GET  /apply/<job_id>          - Apply page
POST /apply/<job_id>          - Submit app
GET  /application/<id>        - View result
GET  /applications            - All apps
POST /resume/<id>/delete      - Delete
GET  /resume/<id>/download    - Download
```

### Recruiter Routes (`/recruiter/*`)
```
GET  /dashboard               - Dashboard
GET  /job/create              - Post form
POST /job/create              - Save job
GET  /job/<id>/edit           - Edit page
POST /job/<id>/edit           - Update
POST /job/<id>/delete         - Delete
GET  /applications            - Manage
POST /application/<id>/update - Status
```

### Admin Routes (`/admin/*`)
```
GET  /dashboard               - Admin dashboard
GET  /users                   - User list
POST /user/<id>/deactivate    - Deactivate
POST /user/<id>/activate      - Activate
GET  /jobs                    - Job list
POST /job/<id>/deactivate     - Deactivate
GET  /analytics               - Reports
```

---

## 🎓 Code Examples

### 1. Register New User
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User(username='john', email='john@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
```

### 2. Create Job Posting
```python
job = Job(
    title='Python Developer',
    description='Build amazing things',
    requirements='Python, Django, PostgreSQL',
    recruiter_id=recruiter.id,
    company=recruiter.company
)
db.session.add(job)
db.session.commit()
```

### 3. Apply for Job
```python
# Get resume and job
resume = Resume.query.get(1)
job = Job.query.get(1)

# Calculate match
result = SkillMatcher.analyze_match(
    resume.extracted_text,
    job.description,
    job.requirements
)

# Create application
app = Application(
    job_id=job.id,
    user_id=current_user.id,
    resume_id=resume.id,
    match_score=result['overall_score'],
    matched_skills=result['matched_skills'],
    missing_skills=result['missing_skills']
)
db.session.add(app)
db.session.commit()
```

---

## 🔧 Configuration

### Change Database
Edit `app/config.py`:
```python
# SQLite (default)
SQLALCHEMY_DATABASE_URI = 'sqlite:///job_portal.db'

# PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/jobportal'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@localhost/jobportal'
```

### Change Port
Edit `run.py`:
```python
app.run(port=5002)  # Change from 5001
```

### Change Upload Folder
Edit `app/config.py`:
```python
UPLOAD_FOLDER = '/path/to/uploads'
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

---

## 📦 Requirements

**Core**: Flask 3.0.0, SQLAlchemy 2.0.23
**Authentication**: Flask-Login 0.6.3, Werkzeug 3.0.1
**PDF**: pdfplumber 0.10.3
**AI/ML**: scikit-learn 1.3.2, numpy 1.26.4
**Forms**: WTForms 3.1.1, Flask-WTF 1.2.1
**Utilities**: python-dotenv 1.0.0, Gunicorn 21.2.0

Install all:
```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment Quick Links

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t job-portal .
docker run -p 5001:5001 job-portal
```

### AWS/DigitalOcean
See SETUP_GUIDE.md for step-by-step instructions

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5001 in use | Change in `run.py` |
| Database not found | Run `python run.py` to create |
| Import errors | Activate virtual environment |
| PDF upload fails | Install pdfplumber: `pip install pdfplumber` |
| Permission denied | Check `uploads/` folder permissions |

See SETUP_GUIDE.md for more troubleshooting.

---

## 📞 Help Resources

1. **README.md** - Features and quick start
2. **SETUP_GUIDE.md** - Detailed guide with examples
3. **PROJECT_SUMMARY.md** - What was built
4. **Code Comments** - Throughout the project
5. **Doc Strings** - All functions documented

---

## 🎯 Learning Path

### Beginner
1. Read README.md
2. Run `python run.py`
3. Register and explore UI
4. Read code comments

### Intermediate
1. Study database models (`app/models/__init__.py`)
2. Trace routes (`app/routes/*.py`)
3. Read SETUP_GUIDE.md examples
4. Modify templates

### Advanced
1. Extend models
2. Add new features
3. Optimize queries
4. Deploy to production

---

## ✅ Checklist Before Starting

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] README.md read
- [ ] App runs: `python run.py`
- [ ] Browser opens: `http://localhost:5001`

---

## 🎉 Ready!

You're all set! Start with:
1. `python run.py` 
2. Open http://localhost:5001
3. Create an account
4. Explore the app!

**Questions?** Check SETUP_GUIDE.md or read the code comments.

**Happy coding!** 🚀

---

**Flask Job Portal**
**Status**: ✅ Production Ready
**Location**: `flask_job_portal/`
**Entry Point**: `run.py`
**Documentation**: 800+ lines
**Code**: 3450+ lines
