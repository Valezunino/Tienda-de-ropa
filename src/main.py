from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .api import register_routes
from .database.dbconfig import engine
from .entities.base import Base
import os

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tienda de Ropa API",
    description="API para gestionar productos de una tienda de ropa",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas de la API
register_routes(app)

# Montar archivos estáticos desde la raíz del proyecto
root_path = os.path.dirname(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=root_path, html=True), name="static")

@app.get("/")
async def root():
    """Servir la página principal del frontend."""
    index_path = os.path.join(root_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Bienvenido a la API de Tienda de Ropa",
        "docs": "/docs",
        "redoc": "/redoc"
    }
