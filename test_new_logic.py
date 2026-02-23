import sqlite3
import os

# Get the resume info
conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()
cursor.execute('SELECT id, filename, user_id FROM resumes WHERE filename = ?', ('popat_sneh_hr.pdf',))
resume = cursor.fetchone()

if resume:
    resume_id, filename, user_id = resume
    print(f'Testing resume: {filename}')
    print(f'Resume ID: {resume_id}')
    print(f'User ID: {user_id}')
    
    # Test the new file finding logic
    uploads_dir = 'uploads'
    user_upload_dir = os.path.join(uploads_dir, user_id)
    actual_file_path = None
    
    if os.path.exists(user_upload_dir):
        # Look for files that contain the resume filename
        for file in os.listdir(user_upload_dir):
            if file.endswith('.pdf') and filename.replace(' ', '_') in file:
                actual_file_path = os.path.join(user_upload_dir, file)
                print(f'Found file: {actual_file_path}')
                print(f'File exists: {os.path.exists(actual_file_path)}')
                break
    
    if not actual_file_path:
        print('File not found with new logic')
else:
    print('Resume not found')

conn.close()
