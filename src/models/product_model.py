from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    id: int
    nombre: str
    talla: str
    color: str
    precio: float
    stock: int
    proveedor: str

    model_config = ConfigDict(from_attributes=True)
