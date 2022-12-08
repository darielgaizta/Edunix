from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from edunix import connection
from auth import schemas as AuthSchemas, services as AuthServices

from . import services, schemas, models

router = APIRouter(
	prefix='/chat',
	tags=['Chats']
)

# Initialize tables
models.connection.Base.metadata.create_all(bind=connection.engine)

# Create chat
@router.post('', status_code=201)
async def create_chat(room_id, chat:schemas.CreateChat, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)) -> schemas.GetChat:
	return await services.create_chat(room_id=room_id, chat=chat, db=db, authenticated_user=authenticated_user)

# Load all chats in a room
@router.get('', response_model=List[schemas.GetChat])
async def load_chats(room_id, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)) -> List[schemas.GetChat]:
	return await services.load_chats(room_id=room_id, db=db, authenticated_user=authenticated_user)