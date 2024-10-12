from http.client import HTTPException
from typing import Annotated

from src.server.database import start_database, create_tables
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, Form, Request, Header
from typing import Union
from pydantic import BaseModel


class RecordBase(BaseModel):
    label: str
    value: str
    record_type: str
    record_class: str
    ttl: int


class RecordCreate(RecordBase):
    pass


class RecordDB(RecordBase):
    id: int

    @staticmethod
    def from_sql_record(record):
        return RecordDB(
            id=record[0],
            label=record[1],
            value=record[2],
            record_type=record[3],
            record_class=record[4],
            ttl=record[5],
        )


conn = start_database()
app = FastAPI()
templates = Jinja2Templates(directory="server/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/records", response_class=HTMLResponse)
async def list_records(
    request: Request, hx_request: Annotated[Union[str, None], Header()] = None
):
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM records")
    sql_records = res.fetchall()
    records = [RecordDB.from_sql_record(record) for record in sql_records]
    print(records)
    return templates.TemplateResponse(
        request=request, name="records.html", context={"records": records}
    )


@app.post("/records", response_class=HTMLResponse)
async def create_record(request: Request, record: Annotated[RecordCreate, Form()]):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO records (label, value, record_type, record_class, ttl)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                record.label,
                record.value,
                record.record_type,
                record.record_class,
                record.ttl,
            ),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException()

    return templates.TemplateResponse(
        request=request, name="records.html", context={"records": [record]}
    )


@app.delete("/records/{id}", response_class=HTMLResponse)
async def delete_record(request: Request, id: int):
    cur = conn.cursor()
    try:
        cur.execute(
            """
            DELETE FROM records WHERE id = ?
        """,
            (id,),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException()

    return templates.TemplateResponse(
        request=request, name="records.html", context={"records": []}
    )


def start_server():
    create_tables(conn)
    uvicorn.run(app, host="0.0.0.0", port=int("2054"))
