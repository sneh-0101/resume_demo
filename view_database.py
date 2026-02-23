#!/usr/bin/env python3
"""
Database Viewer - View all database contents
"""

import sqlite3
import os
from datetime import datetime

def view_database():
    """View all tables and data in the SQLite database"""
    
    # Database path
    db_path = os.path.join('instance', 'app.db')
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("AI Resume Analyzer Database")
        print("=" * 50)
        print(f"Database: {db_path}")
        print(f"Size: {os.path.getsize(db_path):,} bytes")
        print(f"Last Modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
        print()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found in database")
            return
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        print()
        
        # View each table
        for table_name, in tables:
            print(f"TABLE: {table_name.upper()}")
            print("-" * 40)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            if columns:
                print("Columns:")
                for col in columns:
                    print(f"   {col[1]} ({col[2]})")
                print()
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("No data in this table")
                print()
                continue
            
            print(f"Total Records: {count}")
            
            # Get all data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
            rows = cursor.fetchall()
            
            if rows:
                # Print column headers
                col_names = [col[1] for col in columns]
                print("Data (showing first 10 records):")
                print("   " + " | ".join(col_names))
                print("   " + "-" * (len(" | ".join(col_names))))
                
                for row in rows:
                    # Format row for display
                    formatted_row = []
                    for item in row:
                        if item is None:
                            formatted_row.append("NULL")
                        elif isinstance(item, str) and len(item) > 50:
                            formatted_row.append(item[:47] + "...")
                        else:
                            formatted_row.append(str(item))
                    print("   " + " | ".join(formatted_row))
                
                if count > 10:
                    print(f"   ... and {count - 10} more records")
            
            print()
        
        # Close connection
        conn.close()
        
        print("Database viewing completed!")
        
    except Exception as e:
        print(f"Error viewing database: {e}")

if __name__ == "__main__":
    view_database()
