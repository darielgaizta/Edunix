from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from edunix import connection
from auth import schemas as AuthSchemas, services as AuthServices

from . import services, schemas, models

router = APIRouter(
	prefix='/news',
	tags=['News']
)

# Initialize tables
models.connection.Base.metadata.create_all(bind=connection.engine)

# Create new
@router.post('', status_code=201)
async def create_new(new:schemas.CreateNew, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.create_new(new=new, db=db, authenticated_user=authenticated_user)

# Get all news
@router.get('', response_model=List[schemas.GetNew])
async def get_all_news(db:Session=Depends(connection.get_db)):
	return await services.get_all_news(db=db)

# Get detail new
@router.get('/{id}', response_model=schemas.GetNew)
async def get_detail_new(id, db:Session=Depends(connection.get_db)):
	return await services.get_detail_new(id=id, db=db)

# Update new
@router.put('/{id}', status_code=204)
async def update_new(id, request:schemas.New, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.update_new(id=id, request=request, db=db, authenticated_user=authenticated_user)

# Delete new
@router.delete('/{id}', status_code=204)
async def destroy_new(id, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.destroy_new(id=id, db=db, authenticated_user=authenticated_user)