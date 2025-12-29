import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from db import create_all_tables
from .routers import customers, transactions, invoices


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)


@app.get("/")
async def root():
    return {"message": "Hola mundo"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if timezone_str is None:
        return {"error": f"Country code ({iso}) not found."}
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}


@app.get("/time/{iso_code}/{format_code}")
async def time_format(iso_code: str, format_code: str = "24"):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if timezone_str is None:
        return {"error": f"Country code ({iso}) not found."}
    tz = zoneinfo.ZoneInfo(timezone_str)
    if format_code == "12":
        return {"time": datetime.now(tz).strftime("%I:%M %p")}
    elif format_code == "24":
        return {"time": datetime.now(tz).strftime("%H:%M")}
    else:
        return {"error": f"Format code ({format_code}) not supported."}
