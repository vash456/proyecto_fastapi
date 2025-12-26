import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice


app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hola mundo"}

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
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.get("/time/{iso_code}/{format_code}")
async def time(iso_code: str, format_code: str = "24"):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    if (format_code == "12"):
        return {"time": datetime.now(tz).strftime("%I:%M %p")}
    elif (format_code == "24"):
        return {"time": datetime.now(tz).strftime("%H:%M")}
    else:
        return {"error": f"Format code ({format_code}) not supported."}

@app.post("/customers", response_model=Customer)    
async def create_customer(customer_data: CustomerCreate):
    return customer_data
    
@app.post("/transactions")    
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")    
async def create_invoice(invoice_data: Invoice):
    return invoice_data