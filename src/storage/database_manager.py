import sqlite3

DB_PATH = "database/alerts.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        src_ip TEXT,
        attack_type TEXT,
        packet_rate REAL,
        severity INTEGER,
        confidence INTEGER,
        country TEXT,
        isp TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_alert(timestamp, src_ip, attack_type, packet_rate, severity,
                 confidence, country, isp, latitude, longitude):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO alerts (
        timestamp, src_ip, attack_type, packet_rate,
        severity, confidence, country, isp, latitude, longitude
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, src_ip, attack_type, packet_rate,
        severity, confidence, country, isp, latitude, longitude
    ))

    conn.commit()
    conn.close()