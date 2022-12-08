from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from edunix import connection
from auth import schemas as AuthSchemas, services as AuthServices

from . import services, schemas, models

router = APIRouter(
	prefix='/room',
	tags=['Rooms']
)

# Initialize tables
models.connection.Base.metadata.create_all(bind=connection.engine)

# Create new empty room
@router.post('', status_code=201)
async def create_room(name, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.create_room(name=name, db=db, authenticated_user=authenticated_user)

# Get all rooms for forum discussion
@router.get('')
async def get_all_rooms(db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.get_all_rooms(db=db, authenticated_user=authenticated_user)

# Update room for forum discussion
@router.put('/{id}', status_code=204)
async def update_room(id, request:schemas.Room, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.update_room(id=id, request=request, db=db, authenticated_user=authenticated_user)

# Create new room for personal chat
@router.post('/personal', status_code=201)
async def create_room_chat(to_user_id:int, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.create_room_chat(to_user_id=to_user_id, db=db, authenticated_user=authenticated_user)

@router.get('/personal', response_model=List[schemas.GetRoomChatAgg])
async def get_all_room_chat(db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)) -> List[schemas.GetRoomChatAgg]:
	return await services.get_all_room_chat(db=db, authenticated_user=authenticated_user)