import sqlite3

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()
cursor.execute('SELECT id, filename FROM resumes WHERE filename LIKE ?', ('%popat_sneh_hr%',))
resume = cursor.fetchone()
if resume:
    resume_id, filename = resume
    print(f'Found resume: {filename}')
    print(f'Resume ID: {resume_id}')
else:
    print('Resume not found')
conn.close()
