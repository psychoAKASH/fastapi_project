from pydoc import describe
from warnings import deprecated

from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import models
from .database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext

app = FastAPI(
    title='Products API',
    description='Get details for all the products and seller on website',
    terms_of_service='http://www.google.com',
    contact={
        'Develoer name': "Akash",
        'website': 'http://www.google.com',
        'email': 'admin@abc.com',
    },
    license_info={
        'name': 'License',
        'url': 'http://www.google.com'
    },
    # docs_url='/documentation',
    # redoc_url=None

)

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put('/product/{id}', tags=['Products'])
def update_product(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if product.first():
        product.update(request.model_dump())
        db.commit()
        return {'message': 'Product successfully updated'}
    return {'error': 'Product not found'}


@app.delete('/produc/{id}', tags=['Products'])
def del_product(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {f"product deleted with id: {id}"}


@app.get('/product/{id}', response_model=schemas.DisplayProduct, tags=['Products'])
def products(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.get('/products', response_model=List[schemas.DisplayProduct], tags=['Products'])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post('/product', tags=['Products'])
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@app.post('/seller', response_model=schemas.DisplaySeller, tags=['Seller'])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
