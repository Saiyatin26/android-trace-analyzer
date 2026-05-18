import sqlite3

DB_NAME = "events.db"

# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp INTEGER,

        duration_ms REAL,

        event_type TEXT,

        cpu_core INTEGER,

        thread_id INTEGER,

        binder_name TEXT
    )
    """)

    conn.commit()

    conn.close()

    print("\nDatabase Created Successfully!\n")


# =========================================================
# CLEAR OLD EVENTS
# =========================================================

def clear_events():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM events")

    conn.commit()

    conn.close()

    print("Old events cleared!\n")


# =========================================================
# INSERT EVENTS
# =========================================================

def insert_events(events):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    for event in events:

        cursor.execute("""
        INSERT INTO events (

            timestamp,
            duration_ms,
            event_type,
            cpu_core,
            thread_id,
            binder_name

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """, (

            event["timestamp"],
            event["duration_ms"],
            event["event_type"],
            event["cpu_core"],
            event["thread_id"],
            event["binder_name"]

        ))

    conn.commit()

    conn.close()

    print(f"{len(events)} events inserted successfully!\n")


# =========================================================
# FETCH EVENTS
# =========================================================

def fetch_events():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM events
    LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows