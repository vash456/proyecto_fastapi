# Manejo de Facturas

## Descripción

Este proyecto es una aplicación sencilla construida con FastAPI para el manejo de facturas, clientes y transacciones. Utiliza una base de datos SQLite para almacenar los datos y proporciona una API RESTful para interactuar con la aplicación.

## Características

- Gestión de clientes
- Gestión de facturas
- Gestión de transacciones
- API RESTful con documentación automática
- Base de datos SQLite

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **FastAPI**: Framework web para construir APIs
- **SQLModel**: ORM para SQLAlchemy y Pydantic
- **SQLite**: Base de datos
- **Uvicorn**: Servidor ASGI

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd app_fast_api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / macOS
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

La aplicación utiliza SQLite como base de datos. Las tablas se crean automáticamente al iniciar la aplicación mediante el lifespan de FastAPI.

## Ejecutar la aplicación

Para ejecutar la aplicación en modo desarrollo:

```bash
fastapi dev app/main.py
```

La aplicación estará disponible en:

- **API Base**: http://127.0.0.1:8000
- **Documentación Swagger UI**: http://127.0.0.1:8000/docs
- **Documentación ReDoc**: http://127.0.0.1:8000/redoc

## Estructura del Proyecto

```
app_fast_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   └── routers/
│       ├── __init__.py
│       ├── customers.py     # Endpoints para clientes
│       ├── invoices.py      # Endpoints para facturas
│       └── transactions.py  # Endpoints para transacciones
├── db.py                    # Configuración de la base de datos
├── models.py                # Modelos de datos
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Este archivo
└── db.sqlite3               # Base de datos SQLite
```

## Endpoints Principales

### Clientes
- `POST /customers` - Crear un nuevo cliente
- `GET /customers` - Listar todos los clientes
- `GET /customers/{id}` - Obtener un cliente específico
- `PATCH /customers/{id}` - Actualizar un cliente

### Facturas
- `POST /invoices` - Crear una nueva factura
- `GET /invoices` - Listar todas las facturas
- `GET /invoices/{id}` - Obtener una factura específica
- `PATCH /invoices/{id}` - Actualizar una factura

### Transacciones
- `POST /transactions` - Crear una nueva transacción
- `GET /transactions` - Listar todas las transacciones
- `GET /transactions/{id}` - Obtener una transacción específica
- `PATCH /transactions/{id}` - Actualizar una transacción

### Otros
- `GET /` - Mensaje de bienvenida
- `GET /time/{iso_code}` - Obtener la hora actual en un país específico
- `GET /time/{iso_code}/{format}` - Obtener la hora en formato 12h o 24h

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
