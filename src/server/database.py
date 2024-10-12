import sqlite3


def start_database():
    conn = create_connection("database.db")
    create_tables(conn)
    return conn


def create_connection(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_tables(conn):
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                label TEXT NOT NULL, 
                value TEXT NOT NULL,
                record_type TEXT NOT NULL, 
                record_class TEXT DEFAULT 'IN',
                ttl INTEGER DEFAULT 3600
        );"""
    ]

    try:
        cursor = conn.cursor()
        for statement in sql_statements:
            cursor.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
