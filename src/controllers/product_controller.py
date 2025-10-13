from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas.product_schema import ProductCreate, ProductOut, ProductUpdate
from ..database.dbconfig import db_dependency
from ..services.product_service import (
    create_new_product,
    delete_product_by_id,
    get_all_products,
    get_product_by_id,
    update_product_by_id
)

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/create", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(db: db_dependency, payload: ProductCreate):
    """Crear un nuevo producto."""
    return create_new_product(db, payload)


@router.get("/", response_model=list[ProductOut])
async def read_products(db: db_dependency):
    """Obtener todos los productos."""
    return get_all_products(db)


@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int, db: db_dependency):
    """Obtener un producto por su ID."""
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.put("/update/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, payload: ProductUpdate, db: db_dependency):
    """Actualizar un producto por su ID."""
    product = update_product_by_id(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.delete("/delete/{product_id}", response_model=ProductOut)
async def delete_product(product_id: int, db: db_dependency):
    """Eliminar un producto por su ID."""
    product = delete_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product
