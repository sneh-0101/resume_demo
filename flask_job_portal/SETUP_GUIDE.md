# Flask Job Portal - Complete Setup & Documentation Guide

## 📋 Table of Contents
1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Database Models](#database-models)
4. [Feature Overview](#feature-overview)
5. [API Endpoints](#api-endpoints)
6. [Code Examples](#code-examples)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Installation

### Step 1: Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
# Run the application (creates database automatically)
python run.py
```

### Step 5: Create Admin Account (Optional)
```bash
python -c "
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@example.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin account created!')
"
```

### Step 6: Run Development Server
```bash
python run.py
# Visit http://localhost:5001
```

---

## 📁 Project Structure Detailed

### Core Application Structure
```
app/
├── __init__.py
│   └── create_app()        # Flask app factory
│   └── db.init_app()       # Database initialization
│   └── login_manager       # User session management
│
├── config.py
│   ├── DevelopmentConfig   # SQLite, DEBUG=True
│   ├── TestingConfig       # In-memory DB, testing mode
│   └── ProductionConfig    # PostgreSQL, secure settings
│
├── models/__init__.py
│   ├── User model          # 8 tables: user profiles
│   ├── Job model           # Job postings by recruiters
│   ├── Resume model        # Resume uploads and parsing
│   └── Application model   # Job applications tracking
│
├── routes/
│   ├── auth.py             # /auth/* routes (23 lines)
│   ├── main.py             # / routes (45 lines)
│   ├── job_seeker.py       # /seeker/* routes (200+ lines)
│   ├── recruiter.py        # /recruiter/* routes (150+ lines)
│   └── admin.py            # /admin/* routes (100+ lines)
│
├── ai_engine/
│   ├── parser.py           # PDF text extraction
│   └── matcher.py          # Resume-job matching (400+ lines)
│
├── templates/
│   ├── base.html           # Master layout
│   ├── index.html          # Home page
│   ├── auth/               # Login, register
│   ├── job_seeker/         # 8 job seeker pages
│   ├── recruiter/          # 5 recruiter pages
│   └── admin/              # 4 admin pages
│
└── static/
    ├── style.css           # Custom styling
    └── main.js             # Client-side utilities
```

---

## 📊 Database Models

### User Model
```python
class User(db.Model):
    # Authentication
    id: int (primary key)
    username: str (unique)
    email: str (unique)
    password_hash: str
    
    # Profile
    first_name: str
    last_name: str
    phone: str
    bio: str (for job seekers)
    company: str (for recruiters)
    
    # Status
    role: str (job_seeker, recruiter, admin)
    is_active: bool (default: True)
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    resumes: Resume[]
    applications: Application[]
    jobs: Job[]
```

### Job Model
```python
class Job(db.Model):
    # Basic Info
    id: int (primary key)
    title: str
    description: str (full job description)
    requirements: str (required skills/experience)
    
    # Details
    location: str
    salary_min: float
    salary_max: float
    job_type: str (Full-time, Part-time, Remote)
    company: str
    
    # Relations
    recruiter_id: int (foreign key -> User)
    
    # Status
    is_active: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    applications: Application[]
```

### Resume Model
```python
class Resume(db.Model):
    # File Info
    id: int (primary key)
    filename: str
    filepath: str (local storage path)
    
    # Content
    extracted_text: str (PDF text content)
    extracted_skills: JSON (['Python', 'AWS', ...])
    
    # Relations
    user_id: int (foreign key -> User)
    
    # Status
    is_primary: bool (primary resume for matching)
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    applications: Application[]
```

### Application Model
```python
class Application(db.Model):
    # IDs
    id: int (primary key)
    job_id: int (foreign key -> Job)
    user_id: int (foreign key -> User)
    resume_id: int (foreign key -> Resume)
    
    # Status
    status: str (pending, reviewed, shortlisted, rejected, accepted)
    
    # AI Matching Results
    match_score: float (0-100)
    matched_skills: JSON (['Python', 'AWS'])
    missing_skills: JSON (['Kubernetes', 'Docker'])
    
    # User Input
    cover_letter: str
    
    # Timestamps
    applied_at: datetime
    updated_at: datetime
```

---

## 🎯 Feature Overview

### 1. User Authentication
**Routes**: `/auth/*`
- Registration with role selection
- Secure password hashing
- Session management
- Login/logout

**Code Example**:
```python
# Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    user = User(username='john', email='john@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username='john').first()
    if user.check_password('password123'):
        login_user(user)
```

### 2. Job Management (Recruiter)
**Routes**: `/recruiter/*`
- Post new jobs
- Edit existing jobs
- Delete jobs
- View applications

**Code Example**:
```python
# Post job
@recruiter_bp.route('/job/create', methods=['POST'])
def create_job():
    job = Job(
        title='Senior Python Developer',
        description='...',
        recruiter_id=current_user.id,
        company=current_user.company
    )
    db.session.add(job)
    db.session.commit()
```

### 3. Job Application (Job Seeker)
**Routes**: `/seeker/*`
- Browse jobs
- Upload resumes
- Apply for jobs
- Track applications
- AI matching score

**Code Example**:
```python
# Apply for job with AI matching
@job_seeker_bp.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    resume = Resume.query.get(resume_id)
    job = Job.query.get(job_id)
    
    # AI Matching
    result = SkillMatcher.analyze_match(
        resume.extracted_text,
        job.description,
        job.requirements
    )
    
    application = Application(
        job_id=job_id,
        user_id=current_user.id,
        match_score=result['overall_score'],
        matched_skills=result['matched_skills'],
        missing_skills=result['missing_skills']
    )
    db.session.add(application)
    db.session.commit()
```

### 4. AI-Based Matching
**Module**: `app/ai_engine/matcher.py`
- TF-IDF text similarity (40%)
- Skill matching (60%)
- Match level indicators
- Skill extraction

**Code Example**:
```python
from app.ai_engine import SkillMatcher

# Analyze match
result = SkillMatcher.analyze_match(
    resume_text="I know Python, AWS, Docker...",
    job_description="We need a Python developer...",
    job_requirements="Python, AWS, Docker required"
)

# Result:
{
    'overall_score': 85.5,
    'tfidf_score': 82.0,
    'skill_score': 88.0,
    'matched_skills': ['python', 'aws', 'docker'],
    'missing_skills': ['kubernetes'],
    'match_level': 'Excellent'
}
```

### 5. Admin Dashboard
**Routes**: `/admin/*`
- Site statistics
- User management
- Job management
- Analytics

---

## 🛣️ API Endpoints

### Authentication Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/auth/register` | GET, POST | User registration |
| `/auth/login` | GET, POST | User login |
| `/auth/logout` | GET | User logout |

### Main Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/dashboard` | GET | Role-based dashboard redirect |
| `/jobs` | GET | Browse jobs (search, filter) |
| `/job/<id>` | GET | View job details |

### Job Seeker Routes (`/seeker/*`)
| Route | Method | Description |
|-------|--------|-------------|
| `/dashboard` | GET | Job seeker dashboard |
| `/resume/upload` | GET, POST | Upload resume |
| `/apply/<job_id>` | GET, POST | Apply for job |
| `/application/<app_id>` | GET | View application |
| `/applications` | GET | View all applications |
| `/resume/<id>/delete` | POST | Delete resume |
| `/resume/<id>/download` | GET | Download resume |

### Recruiter Routes (`/recruiter/*`)
| Route | Method | Description |
|-------|--------|-------------|
| `/dashboard` | GET | Recruiter dashboard |
| `/job/create` | GET, POST | Create job posting |
| `/job/<id>/edit` | GET, POST | Edit job |
| `/job/<id>/delete` | POST | Delete job |
| `/applications` | GET | Manage applications |
| `/application/<id>/update` | POST | Update app status |

### Admin Routes (`/admin/*`)
| Route | Method | Description |
|-------|--------|-------------|
| `/dashboard` | GET | Admin dashboard |
| `/users` | GET | Manage users |
| `/user/<id>/deactivate` | POST | Deactivate user |
| `/user/<id>/activate` | POST | Activate user |
| `/jobs` | GET | Manage jobs |
| `/job/<id>/deactivate` | POST | Deactivate job |
| `/analytics` | GET | View analytics |

---

## 💡 Code Examples

### Example 1: Create a Job Seeker Account
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Create user
    user = User(
        username='alice',
        email='alice@example.com',
        first_name='Alice',
        last_name='Smith',
        role='job_seeker'
    )
    user.set_password('secure_password')
    db.session.add(user)
    db.session.commit()
    print(f"User {user.username} created!")
```

### Example 2: Post a Job (as Recruiter)
```python
from app import create_app, db
from app.models import Job, User

app = create_app()
with app.app_context():
    recruiter = User.query.filter_by(username='recruiter').first()
    
    job = Job(
        title='Python Developer',
        description='Build amazing things with Python...',
        requirements='Python, Django, PostgreSQL, Docker',
        location='New York, USA',
        salary_min=100000,
        salary_max=150000,
        job_type='Full-time',
        company='Tech Corp',
        recruiter_id=recruiter.id
    )
    db.session.add(job)
    db.session.commit()
    print(f"Job '{job.title}' posted!")
```

### Example 3: AI Matching
```python
from app.ai_engine import SkillMatcher

resume_text = """
Senior Python Developer with 5 years experience
Skills: Python, Django, FastAPI, PostgreSQL, AWS, Docker, Kubernetes
"""

job_description = """
We're hiring a Python Developer
Build backend services using Python and Django
"""

job_requirements = """
Required: Python, Django, PostgreSQL, Docker
Nice to have: AWS, Kubernetes, FastAPI
"""

result = SkillMatcher.analyze_match(
    resume_text,
    job_description,
    job_requirements
)

print(f"Overall Score: {result['overall_score']}%")
print(f"Matched Skills: {result['matched_skills']}")
print(f"Missing Skills: {result['missing_skills']}")
print(f"Match Level: {result['match_level']}")
```

### Example 4: Query Applications
```python
from app import create_app, db
from app.models import Application

app = create_app()
with app.app_context():
    # Get all shortlisted applications
    shortlisted = Application.query.filter_by(status='shortlisted').all()
    
    # Get high-match applications (>80%)
    high_match = Application.query.filter(
        Application.match_score > 80
    ).all()
    
    # Get applications by user
    user_apps = Application.query.filter_by(user_id=1).all()
    
    for app in user_apps:
        print(f"{app.user.get_full_name()} - {app.job.title}: {app.match_score}%")
```

---

## 🔍 Troubleshooting

### Issue 1: Database File Not Found
**Solution**: Database creates automatically on first run
```bash
python run.py  # Creates job_portal.db
```

### Issue 2: Import Errors
**Solution**: Ensure virtual environment is activated
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue 3: Port Already in Use
**Solution**: Change port in `run.py`
```python
if __name__ == '__main__':
    app.run(port=5002)  # Change from 5001 to 5002
```

### Issue 4: PDF Upload Failed
**Solution**: Ensure pdfplumber is installed
```bash
pip install pdfplumber
```

### Issue 5: Permissions Error
**Solution**: Check upload folder permissions
```bash
# macOS/Linux
chmod -R 755 uploads/

# Or in Python
import os
os.makedirs('uploads', mode=0o755, exist_ok=True)
```

### Issue 6: Password Check Failed
**Solution**: Ensure password is at least 6 characters
```python
if len(password) >= 6:
    user.set_password(password)
```

---

## 🚀 Next Steps

1. **Customize**: Edit templates in `/templates/`
2. **Add Features**: Extend routes and models
3. **Deploy**: Follow deployment guide
4. **Optimize**: Add caching, indexing, search
5. **Test**: Write unit tests for models/routes
6. **Monitor**: Add logging and error tracking

---

**Happy building!** 🎉
