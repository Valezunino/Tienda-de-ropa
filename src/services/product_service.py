from sqlalchemy.orm import Session
from src.entities.product_entity import Product
from src.schemas.product_schema import ProductCreate, ProductUpdate

def create_new_product(db: Session, product: ProductCreate):
    new_product = Product(
        nombre=product.nombre,
        talla=product.talla,
        color=product.color,
        precio=product.precio,
        stock=product.stock,
        proveedor=product.proveedor
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def update_product_by_id(db: Session, product_id: int, product_update: ProductUpdate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    db.delete(product)
    db.commit()
    return product
