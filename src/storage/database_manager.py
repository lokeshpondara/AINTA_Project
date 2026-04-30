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
        longitude REAL,
        risk_score REAL DEFAULT 0,
        priority TEXT DEFAULT 'LOW',
        mitre_tactic TEXT DEFAULT 'unknown',
        mitre_technique TEXT DEFAULT 'unknown'
    )
    """)
    cursor.execute("PRAGMA table_info(alerts)")
    print("DB schema updated")

    conn.commit()
    conn.close()


def insert_alert(timestamp, src_ip, attack_type, packet_rate, severity,
                 confidence=0, country='unknown', isp='unknown', latitude=0.0, longitude=0.0, risk_score=0, priority='LOW', mitre_tactic='unknown', mitre_technique='unknown'):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO alerts (
        timestamp, src_ip, attack_type, packet_rate,
        severity, confidence, country, isp, latitude, longitude
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, src_ip, attack_type, packet_rate, severity, confidence, country, isp, latitude, longitude))

    conn.commit()
    conn.close()
