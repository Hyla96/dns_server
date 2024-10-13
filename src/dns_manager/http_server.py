from http.client import HTTPException
from fastapi import Depends

from src.dns_manager.database import create_tables, conn, RecordDB, RecordBase
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi import FastAPI, Request

from src.udp_server.record_type import RecordType

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

    for record in records:
        if record.record_type == RecordType.A:
            record.value = ".".join([str(integer) for integer in record.value])
        elif record.record_type == RecordType.CNAME:
            record.value = record.value.decode("ascii")

    return templates.TemplateResponse(
        request=request, name="records.html", context={"records": records}
    )


def validate_record(record: RecordBase):
    return RecordBase.model_validate(record.dict())


@app.post("/records", response_class=HTMLResponse)
async def create_record(
    request: Request, record: RecordBase = Depends(validate_record)
):
    cur = conn.cursor()
    try:
        if record.record_type not in [RecordType.A, RecordType.CNAME]:
            raise HTTPException()

        if record.record_type == RecordType.A:
            integers = record.value.decode("ascii").split(".")
            if len(integers) != 4:
                raise HTTPException()
            for integer in integers:
                if not 0 <= int(integer) <= 255:
                    raise HTTPException()

            value = bytes([int(integer) for integer in integers])
        else:
            value = record.value

        print(value)
        cur.execute(
            """
            INSERT INTO records (label, value, record_type, record_class, ttl)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                record.label,
                value,
                record.record_type.value,
                record.record_class.value,
                record.ttl,
            ),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException()

    if record.record_type == RecordType.A:
        record.value = ".".join([str(integer) for integer in record.value])
    elif record.record_type == RecordType.CNAME:
        record.value = record.value.decode("ascii")

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
