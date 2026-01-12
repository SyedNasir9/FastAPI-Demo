from fastapi import FastAPI
from pydantic import BaseModel
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return {"message": "Welcome to Inventory Management System"}

products = [
    {"id": 1, "name": "Laptop", "description": "A high-performance laptop", "price": 999.99, "quantity": 10},
    {"id": 2, "name": "Smartphone", "description": "A latest model smartphone", "price": 699.99, "quantity": 25},
    {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones", "price": 199.99, "quantity": 15}, 
    {"id": 4, "name": "Monitor", "description": "4K UHD Monitor", "price": 399.99, "quantity": 8    },
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product["id"] == id:
            return product

    return {"message": "PRODUCT NOT FOUND"}

@app.post("/product")
def add_product(product: Product):
    products.append(product.dict())
    return {"message": product.name + " added successfully"}