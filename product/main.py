from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import models
from .database import engine, SessionLocal
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put('/product/{id}')
def update_product(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first():
        product.update(request.model_dump())
        db.commit()
        return {'message': 'Product successfully updated'}
    return {'error': 'Product not found'}


@app.delete('/produc/{id}')
def del_product(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {f"product deleted with id: {id}"}


@app.get('/product/{id}', response_model=schemas.DisplayProduct)
def products(id, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.id == id).first()
    return products


@app.get('/products', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post('/product')
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request
