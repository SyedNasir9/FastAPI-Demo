from fastapi import FastAPI, Depends
from pydantic import BaseModel
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Welcome to Inventory Management System"}

products = [
    {"id": 1, "name": "Laptop", "description": "A high-performance laptop", "price": 999.99, "quantity": 10},
    {"id": 2, "name": "Smartphone", "description": "A latest model smartphone", "price": 699.99, "quantity": 25},
    {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones", "price": 199.99, "quantity": 15}, 
    {"id": 4, "name": "Monitor", "description": "4K UHD Monitor", "price": 399.99, "quantity": 8    },
]

def get_db():
    db = session()
    try:
        yield db
    finally:    
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product))
        db.commit()
init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
         return db_product
    return {"message": "PRODUCT NOT FOUND"}

@app.post("/product")
def add_product(product: Product):
    products.append(product.dict())
    return {"message": product.name + " added successfully"} 

@app.put("/product")
def update_product(id: int, product: Product):
      for i in range(len(products)):
          if products[i]["id"] == id:
             products[i] = product
             return {"message": "Product updated successfully"}
          
      return {"message": "PRODUCT NOT FOUND"}    

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i]["id"] == id:
            del products[i]
            return {"message": "Product deleted successfully"}
        
    return {"message": "PRODUCT NOT FOUND"}        