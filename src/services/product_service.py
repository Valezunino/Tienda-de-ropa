from sqlalchemy.orm import Session
from ..schemas.product_schema import ProductCreate, ProductUpdate
from ..entities.product_entity import Productos

def create_new_product(db: Session,
                       product: ProductCreate):
    new_product = Productos (
        
        Producto = product.Producto,
        Talla = product.Talla,
        Color = product.Color,
        Precio = product.Precio,
        Stock = product.Stock,
        Proveedores = product.Proveedores
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_all_products(db: Session):
    return db.query(Productos).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Productos).filter(Productos.ProductosID == product_id).first()

def update_product_by_id(db: Session, product_id: int, 
                         product_update: ProductUpdate):
    product = db.query(Productos).filter(Productos.ProductosID == product_id).first()
    if product:
        product.Producto = product_update.Producto if product_update.Producto is not None else product.Producto
        product.Talla = product_update.Talla if product_update.Talla is not None else product.Talla
        product.Color = product_update.Color if product_update.Color is not None else product.Color
        product.Precio = product_update.Precio if product_update.Precio is not None else product.Precio
        product.Stock = product_update.Stock if product_update.Stock is not None else product.Stock
        product.Proveedores = product_update.Proveedores if product_update.Proveedores is not None else product.Proveedores
      
        db.commit()
        db.refresh(product)
        return product
    return None

def delete_product_by_id(db: Session, product_id: int):
    product = db.query(Productos).filter(Productos.ProductosID == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False