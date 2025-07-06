import sqlite3
import time

def log_incident(cpu_usage, analysis, action):
    # Connect to (or create) database
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            timestamp TEXT,
            cpu_usage REAL,
            analysis TEXT,
            action TEXT
        )
    """)

    # Insert the incident record
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO incidents VALUES (?, ?, ?, ?)", 
                   (timestamp, cpu_usage, analysis, action))

    # Save changes and close
    conn.commit()
    conn.close()
