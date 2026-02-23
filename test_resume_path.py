import sqlite3
import os

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()
cursor.execute('SELECT id, filename, user_id FROM resumes WHERE user_id = ? LIMIT 1', ('b96390ad-3053-49eb-b402-ae8157729089',))
resume = cursor.fetchone()
if resume:
    resume_id, filename, user_id = resume
    print(f'Testing resume: {filename}')
    print(f'Resume ID: {resume_id}')
    print(f'User ID: {user_id}')
    
    # Test the file path logic
    uploads_dir = 'uploads'
    possible_paths = [
        os.path.join(uploads_dir, user_id, f'{resume_id}_{filename}'),
        os.path.join(uploads_dir, user_id, f'{resume_id}_{filename.replace(" ", "_")}'),
    ]
    
    for path in possible_paths:
        exists = os.path.exists(path)
        print(f'Path: {path} - Exists: {exists}')
else:
    print('No resume found')
conn.close()
