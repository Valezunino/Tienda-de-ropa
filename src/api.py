from fastapi import FastAPI
from .controllers.product_controller import router as products_router

def register_routes(app: FastAPI):
    app.include_router(products_router)