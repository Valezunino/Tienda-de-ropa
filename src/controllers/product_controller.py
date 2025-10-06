"""Product controller for handling product-related API endpoints."""

from fastapi import APIRouter
from src.schemas.product_schema import ProductCreate, ProductOut, ProductUpdate
from src.database.dbconfig import db_dependency
from src.services.product_service import (
    create_new_product,
    delete_product_by_id,
    get_all_products,
    get_product_by_id,
    update_product_by_id
)
router = APIRouter()

@router.post("/create", response_model=ProductOut, status_code=201)
async def create_product(db: db_dependency, payload: ProductCreate):
    """Crear un nuevo producto."""
    return create_new_product(db, payload)

@router.get("/")
async def read_products(db: db_dependency):
    """Obtener todos los productos."""
    return get_all_products(db)

@router.get("/{productosID}")
async def read_product(productosID: int, db: db_dependency):
    """Obtener un producto por su ID."""
    return get_product_by_id(db, productosID)

@router.put("/update/{productosID}")
async def update_product(
    productosID: int, payload: ProductUpdate,
    db: db_dependency
):
    """Actualizar un producto por su ID."""
    return update_product_by_id(db, productosID, payload)

@router.delete("/delete/{productosID}")
async def delete_product(productosID: int, db: db_dependency):
    """Eliminar un producto por su ID."""
    return delete_product_by_id(db, productosID)
