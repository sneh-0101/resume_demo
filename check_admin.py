import sqlite3

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

# Check for admin users
cursor.execute('SELECT username, email, is_admin, role FROM users WHERE is_admin = 1 OR role = "admin"')
admins = cursor.fetchall()

if admins:
    print('Existing Admin Users:')
    for admin in admins:
        print(f'  - {admin[0]} ({admin[1]}) - Role: {admin[3]}')
else:
    print('No admin users found. You need to create an admin account.')

conn.close()
