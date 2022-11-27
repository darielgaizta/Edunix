from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from edunix import connection

from . import models, schemas, services

router = APIRouter(
	prefix='/auth',
	tags=['Authentication']
)

@router.post('/login')
def login(db:Session=Depends(connection.get_db), request:OAuth2PasswordRequestForm=Depends()):
	return services.login(request=request, db=db)
