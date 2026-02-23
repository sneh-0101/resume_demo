from flask_app import create_app, db
from flask_app.models import User, Resume, JobPosting, Analysis
import os
import traceback

app = create_app()

def seed_database():
    with app.app_context():
        # 1. Close any existing connections and remove DB file
        db.session.remove()
        db_path = os.path.join(app.instance_path, 'app.db')
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Removed existing database at {db_path}")
            except Exception as e:
                print(f"Warning: Could not remove database file: {e}")
                # Try dropping all instead
                db.drop_all()
        
        # 2. Create tables
        db.create_all()
        print("Created all tables.")

        try:
            # 3. Create Users
            admin = User(username='admin', email='admin@example.com', first_name='System', last_name='Admin', is_admin=True, role='admin')
            admin.set_password('admin123')
            
            test_user = User(username='user', email='user@example.com', first_name='Jane', last_name='Doe', is_admin=False, role='user')
            test_user.set_password('user123')
            
            hr_user = User(username='hr', email='hr@example.com', first_name='HR', last_name='Manager', is_admin=False, role='hr')
            hr_user.set_password('hr123')
            
            db.session.add_all([admin, test_user, hr_user])
            db.session.flush() # Get IDs

            # 4. Create Demo Job Posting (HR)
            demo_jd_text = """
            Senior Python Developer - Innovation Labs
            
            About the Role:
            We are looking for a Senior Python Developer to join our core backend team. You will be responsible for building scalable APIs, optimizing database performance, and mentoring junior developers.
            
            Requirements:
            - 5+ years of experience with Python and Flask/Django
            - Strong knowledge of PostgreSQL and Redis
            - Experience with Cloud platforms (AWS/GCP)
            - Mentorship experience and clean code principles
            
            Sections: Experience, Education, Skills, Contact
            """
            
            demo_job = JobPosting(
                title='Senior Python Developer',
                company='Innovation Labs',
                description=demo_jd_text,
                required_skills=['Python', 'Flask', 'PostgreSQL', 'Redis', 'AWS', 'API Design'],
                location='Remote / New York',
                posted_by=hr_user.id
            )
            db.session.add(demo_job)
            
            # 5. Create Demo Resume (User)
            demo_resume_text = """
            Jane Doe - Python Expert
            Email: jane.doe@example.com | Phone: +1-555-0199
            
            Summary:
            Experienced Full Stack Developer with 7 years of specialized experience in Python backend development.
            
            Skills:
            Python, Flask, Django, PostgreSQL, AWS, Docker, Git, REST APIs, Mentorship.
            
            Experience:
            Senior Software Engineer | Tech Solutions (2018 - Present)
            - Built scalable microservices using Python and Flask.
            - Optimized database queries reducing latency by 40%.
            - Led a team of 4 developers.
            
            Education:
            B.S. in Computer Science | University of Technology
            """
            
            # Create a dummy file for the resume
            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            resume_filename = 'jane_doe_resume.pdf'
            resume_path = os.path.join(upload_folder, resume_filename)
            with open(resume_path, 'w') as f:
                f.write("Demo PDF Content Placeholder")
            
            demo_resume = Resume(
                user_id=test_user.id,
                filename=resume_filename,
                filepath=resume_path,
                extracted_text=demo_resume_text,
                extracted_skills=['Python', 'Flask', 'Django', 'PostgreSQL', 'AWS', 'Git', 'REST APIs', 'Mentorship']
            )
            db.session.add(demo_resume)
            db.session.flush()
            
            # 6. Create Demo Analysis
            demo_analysis = Analysis(
                user_id=test_user.id,
                resume_id=demo_resume.id,
                job_id=demo_job.id,
                job_description=demo_jd_text,
                match_score=85.5,
                matched_skills=['Python', 'Flask', 'PostgreSQL', 'AWS'],
                missing_skills=['Redis', 'API Design'],
                suggestions=[
                    "Highlight your experience with Redis more clearly.",
                    "Add specific examples of 'API Design' projects to your experience section."
                ],
                match_percentage=85,
                ats_score=92.0,
                ats_details={
                    'findings': [
                        "Contact information is well-formatted.",
                        "Standard section headers detected correctly.",
                        "Clear focus on backend technologies."
                    ]
                }
            )
            db.session.add(demo_analysis)
            
            # 7. Final Commit
            db.session.commit()
            print("Successfully seeded database with demo examples!")
            
        except Exception as e:
            print(f"Error during seeding: {e}")
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    seed_database()
