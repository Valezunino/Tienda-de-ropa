from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    ProductosID: int
    Producto : str
    Talla: str
    Color: str
    Precio: float
    Stock: int
    Proveedores: str

    model_config = ConfigDict(from_attributes=True)