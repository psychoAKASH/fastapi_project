from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller

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

app.include_router(product.router)
app.include_router(seller.router)

models.Base.metadata.create_all(engine)
