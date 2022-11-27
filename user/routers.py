from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from edunix import connection

from . import models, schemas, services

router = APIRouter(
	prefix='/user',
	tags=['Users']
)

# Initialize table to database
models.connection.Base.metadata.create_all(bind=connection.engine)

# Create user
@router.post('', status_code=201)
async def create_user(user:schemas.CreateUser, db:Session=Depends(connection.get_db)):
	return await services.create_user(user=user, db=db)

# Get all users
@router.get('', response_model=List[schemas.GetUser])
async def get_all_users(db:Session=Depends(connection.get_db)):
	return await services.get_all_users(db=db)
