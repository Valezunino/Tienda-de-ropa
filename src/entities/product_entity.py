from typing import Optional
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Product(Base):
    __tablename__ = "Productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    talla: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(String(255), nullable=True)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    proveedor: Mapped[str] = mapped_column(String(255), nullable=True)
