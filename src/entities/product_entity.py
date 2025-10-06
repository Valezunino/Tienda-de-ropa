from typing import Optional
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Productos(Base):
    __tablename__ = "Productos"

    ProductosID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Producto: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    Talla : Mapped[str] = mapped_column(String(255), nullable=False)
    Color: Mapped[str] = mapped_column(Float, nullable=False)
    Precio: Mapped[float] = mapped_column(Float)
    Stock: Mapped[Optional[int]] = mapped_column(Integer, nullable= True)
    Proveedores: Mapped [str] = mapped_column(String(255)) 