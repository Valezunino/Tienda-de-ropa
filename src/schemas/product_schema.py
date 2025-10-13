from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    nombre: str
    talla: Optional[str] = None
    color: Optional[str] = None
    precio: float
    stock: Optional[int] = None
    proveedor: Optional[str] = None


class ProductCreate(ProductBase):
    """Esquema para crear un producto."""
    pass


class ProductUpdate(BaseModel):
    """Esquema para actualizar un producto."""
    nombre: Optional[str] = None
    talla: Optional[str] = None
    color: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    proveedor: Optional[str] = None


class ProductOut(ProductBase):
    """Esquema de salida (para mostrar productos)."""
    id: int
    model_config = ConfigDict(from_attributes=True)

