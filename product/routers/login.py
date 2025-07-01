from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models
from ..database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..schemas import Tokendata

SECRET_KEY = '29195b60f0e609e576b98813c0f0fda92cb8c4290e3f68c4931a5026abd51324'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(
    tags=['Login'],
    prefix='/login'
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found or invalid user.")
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Password')
    access_token = generate_token(data={'sub': seller.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid auth credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = Tokendata(username=username)
    except JWTError:
        raise credentials_exception
