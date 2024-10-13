import sqlite3
from pydantic import BaseModel


class RecordBase(BaseModel):
    label: str
    value: str
    record_type: str
    record_class: str
    ttl: int


class RecordDB(RecordBase):
    id: int

    @staticmethod
    def from_sql_record(record):
        if record is None:
            return None
        return RecordDB(
            id=record[0],
            label=record[1],
            value=record[2],
            record_type=record[3],
            record_class=record[4],
            ttl=record[5],
        )


def create_connection(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename, check_same_thread=False)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_tables():
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


def get_record(label, record_type, record_class):
    print(f"Getting record {label}, {record_type}, {record_class}")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM records WHERE label=? AND record_class=? AND record_type=?",
        (
            label,
            record_class,
            record_type,
        ),
    )
    return RecordDB.from_sql_record(cur.fetchone())


conn = create_connection("database.db")
