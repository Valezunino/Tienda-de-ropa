from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict

class Productos(BaseModel):
    ProductoID: int
    Producto : str
    Talla : str
    color : str
    precio : float
    Stock : int
    Proveedores : str

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool = True
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
