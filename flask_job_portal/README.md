# Flask Job Portal - Complete Starter Project

A production-ready Flask-based job portal application with AI-powered resume matching, multi-role authentication, and comprehensive job management system.

## 🎯 Features

### User Roles & Authentication
- **Job Seeker**: Browse jobs, upload resumes, apply for positions, track applications
- **Recruiter**: Post jobs, manage applications, review candidates
- **Admin**: Site administration, user management, analytics

### Core Functionality
- ✅ User registration and authentication with role-based access
- ✅ Resume upload and PDF parsing
- ✅ AI-based resume-to-job matching using TF-IDF and skill analysis
- ✅ Job posting and management
- ✅ Application tracking with match scores
- ✅ Dashboard for each user role
- ✅ Real-time job statistics

### AI-Powered Matching
- TF-IDF text similarity analysis
- Skill extraction and matching (100+ technical skills database)
- Hybrid scoring algorithm (40% TF-IDF + 60% skill match)
- Match quality indicators (Excellent/Good/Fair/Poor)

## 📁 Project Structure

```
flask_job_portal/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration (Dev/Test/Prod)
│   ├── models/                  # Database models
│   │   └── __init__.py          # User, Job, Resume, Application models
│   ├── routes/                  # Application routes/controllers
│   │   ├── __init__.py
│   │   ├── auth.py              # Login, register, logout
│   │   ├── main.py              # Home page, job browsing
│   │   ├── job_seeker.py        # Job seeker dashboard and applications
│   │   ├── recruiter.py         # Recruiter job posting and management
│   │   └── admin.py             # Admin dashboard and analytics
│   ├── ai_engine/               # AI modules
│   │   ├── __init__.py
│   │   ├── parser.py            # PDF resume parser
│   │   └── matcher.py           # Resume-job matching engine
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Master layout
│   │   ├── index.html           # Home page
│   │   ├── auth/                # Login, register
│   │   ├── job_seeker/          # Job seeker pages
│   │   ├── recruiter/           # Recruiter pages
│   │   └── admin/               # Admin pages
│   └── static/                  # CSS, JavaScript
│       ├── style.css            # Custom styling
│       └── main.js              # Client-side utilities
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
cd flask_job_portal
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python run.py
```

The app will run on `http://localhost:5001`

## 🔧 Configuration

Edit `app/config.py` to customize:
- Database URL
- Upload folder
- File size limits
- Session settings

### Environment Variables
Create `.env` file:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///job_portal.db
```

## 👤 User Roles

### Job Seeker
- Browse available jobs
- Upload resume (PDF)
- Apply for jobs with cover letter
- View match scores and feedback
- Track application status

Route: `/seeker/*`

### Recruiter
- Post new job listings
- Edit/delete job postings
- Review applications
- View candidate resumes
- Update application status

Route: `/recruiter/*`

### Admin
- View site statistics
- Manage all users
- Manage all jobs
- View analytics and reports
- Deactivate/activate users

Route: `/admin/*`

## 🤖 AI Matching Engine

The `SkillMatcher` class provides intelligent resume-to-job matching:

```python
from app.ai_engine import SkillMatcher

# Analyze match between resume and job
result = SkillMatcher.analyze_match(
    resume_text="Python, Java, AWS...",
    job_description="Senior Backend Engineer",
    job_requirements="Python, AWS, Docker"
)

# Returns:
# {
#     'overall_score': 85.5,           # Final match score
#     'tfidf_score': 82.0,             # Text similarity
#     'skill_score': 88.0,             # Skill match percentage
#     'matched_skills': ['python', 'aws', 'docker'],
#     'missing_skills': ['kubernetes'],
#     'match_level': 'Excellent'
# }
```

### Skill Database
100+ technical and soft skills including:
- Languages: Python, Java, JavaScript, C++, etc.
- Frameworks: React, Vue, Django, Flask, Spring, etc.
- Databases: MySQL, MongoDB, PostgreSQL, Redis, etc.
- Cloud: AWS, Azure, GCP
- Tools: Docker, Kubernetes, Git, Jenkins
- Soft Skills: Leadership, Communication, Teamwork

## 📊 Database Models

### User
- id, username, email, password_hash
- role (job_seeker, recruiter, admin)
- first_name, last_name, phone, bio
- company (for recruiters)
- is_active, created_at, updated_at

### Job
- id, title, description, requirements
- location, salary_min, salary_max
- job_type (Full-time, Part-time, Remote)
- company, recruiter_id
- is_active, created_at, updated_at

### Resume
- id, user_id, filename, filepath
- extracted_text, extracted_skills (JSON)
- is_primary, created_at, updated_at

### Application
- id, job_id, user_id, resume_id
- status (pending, reviewed, shortlisted, rejected, accepted)
- match_score, matched_skills, missing_skills
- cover_letter, applied_at, updated_at

## 🔐 Security Features

- Password hashing with Werkzeug (PBKDF2)
- CSRF token protection on forms
- SQL injection prevention via SQLAlchemy ORM
- Session management with secure cookies
- File upload validation (type and size)
- Role-based access control

## 📦 Dependencies

- **Flask 3.0.0** - Web framework
- **SQLAlchemy 2.0.23** - ORM
- **Flask-Login 0.6.3** - User sessions
- **scikit-learn 1.3.2** - ML for TF-IDF
- **pdfplumber 0.10.3** - PDF parsing
- **WTForms 3.1.1** - Form validation

## 🧪 Testing

```bash
# Run tests (if available)
pytest tests/

# Test database operations
python -c "from app import create_app, db; app = create_app('testing'); db.create_all()"
```

## 📝 Example Usage

### Creating a Job Seeker Account
1. Navigate to `/auth/register`
2. Select "Job Seeker" role
3. Fill in details and password
4. Login with credentials

### Posting a Job (as Recruiter)
1. Login as recruiter
2. Go to `/recruiter/job/create`
3. Fill job details (title, description, requirements, salary)
4. Submit to post job

### Applying for a Job (as Job Seeker)
1. Login as job seeker
2. Upload resume at `/seeker/resume/upload`
3. Browse jobs at `/jobs`
4. Click "Apply" and select resume
5. View match score (AI-calculated)
6. Track application status in dashboard

## 🚢 Deployment

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
1. Set up Flask app on server
2. Use Gunicorn as WSGI server
3. Configure Nginx as reverse proxy
4. Set up PostgreSQL database
5. Configure SSL/HTTPS

## 📈 Future Enhancements

- [ ] Email notifications for applications
- [ ] LinkedIn profile import
- [ ] Advanced search and filtering
- [ ] Job recommendations using ML
- [ ] Video interview integration
- [ ] Payment system for premium features
- [ ] API endpoints for mobile app
- [ ] Real-time chat between recruiter and candidate
- [ ] Skill assessment tests
- [ ] Resume parser with OCR

## 🤝 Contributing

This is a starter project. Feel free to:
- Add more features
- Improve UI/UX
- Optimize algorithms
- Write tests
- Submit pull requests

## 📄 License

This project is open source and available for educational purposes.

## 📞 Support

For issues or questions:
1. Check the code comments
2. Review database models
3. Examine route handlers
4. Test with sample data

---

**Happy coding!** 🚀

Built with ❤️ using Flask
