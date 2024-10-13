from http.client import HTTPException
from typing import Annotated

from src.dns_manager.database import create_tables, conn, RecordDB, RecordBase
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, Form, Request


app = FastAPI()
templates = Jinja2Templates(directory="dns_manager/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/records", response_class=HTMLResponse)
async def list_records(
    request: Request,
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
async def create_record(request: Request, record: Annotated[RecordBase, Form()]):
    cur = conn.cursor()
    try:
        if record.record_type not in ["A", "CNAME"]:
            raise HTTPException()

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


def start_http_server():
    create_tables()
    uvicorn.run(app, host="0.0.0.0", port=int("2054"))
