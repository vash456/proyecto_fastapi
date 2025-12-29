# Manejo de Facturas

Proyecto sencillo con FastAPI para el manejo de facturas.

## Crear entorno virtual

    python -m venv venv

## Activar entorno virtual

### Windows

    venv\Scripts\activate

### Linux / macOS

    source venv/bin/activate

## Instalar dependencias

    pip install -r requirements.txt

## Ejecutar la aplicación

    fastapi dev app/main.py

La aplicación estará disponible en:

- <http://127.0.0.1:8000>
- <http://127.0.0.1:8000/docs>
- <http://127.0.0.1:8000/redoc>

## Estructura del proyecto

    app/
    ├── __init__.py
    ├── main.py
    ├── routers/
    │   ├── __init__.py
    │   ├── customers.py
    │   ├── invoices.py
    │   └── transactions.py
    db.py
    models.py
    README.md
    requirements.txt
    

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- Uvicorn

