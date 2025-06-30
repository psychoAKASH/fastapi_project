from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found or invalid user.")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Password')
    # Generate the JWT token
    return request
