import sqlite3
from typing import Union

from pydantic import BaseModel, Field

from src.packet.record_class import RecordClass
from src.packet.record_type import RecordType


class RecordBase(BaseModel):
    label: str
    value: Union[bytes, str] = Field(..., alias="value")
    record_type: Union[RecordType, int] = Field(..., alias="record_type")
    record_class: Union[RecordClass, int] = Field(..., alias="record_class")
    ttl: int

    @classmethod
    def model_validate(cls, obj):
        if isinstance(obj.get("record_type"), str):
            obj["record_type"] = RecordType.from_int(int(obj["record_type"]))
        elif isinstance(obj.get("record_type"), int):
            obj["record_type"] = RecordType.from_int(obj["record_type"])

        if isinstance(obj.get("record_class"), str):
            obj["record_class"] = RecordClass.from_int(int(obj["record_class"]))
        elif isinstance(obj.get("record_class"), int):
            obj["record_class"] = RecordClass.from_int(obj["record_class"])

        return super().model_validate(obj)


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
            record_type=RecordType.from_int(record[3]),
            record_class=RecordClass.from_int(record[4]),
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
                value BLOB NOT NULL,
                record_type INTEGER NOT NULL, 
                record_class INTEGER NOT NULL,
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


def get_record(label: str, record_type: RecordType, record_class: RecordClass):
    print(f"Getting record {label}, {record_type}, {record_class}")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM records WHERE label=? AND record_class=? AND record_type=?",
        (
            label,
            record_class.value,
            record_type.value,
        ),
    )
    return RecordDB.from_sql_record(cur.fetchone())


conn = create_connection("database.db")
