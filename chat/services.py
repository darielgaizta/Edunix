from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth import schemas as AuthSchemas
from room import schemas as RoomSchemas

from . import models, schemas

# Create chat
async def create_chat(room_id, chat:schemas.CreateChat, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetChat:
	# Room validation
	room = db.query(models.Room).filter(models.Room.id==room_id)
	if not room.first():
		raise HTTPException(status_code=404, detail=f'Room with ID {room_id} does not exists.')
	# Intantiate Chat
	new_chat = models.Chat(**chat.dict(), user_id=authenticated_user.id, room_id=room_id)
	db.add(new_chat)
	db.commit()
	# Return the newly created chat
	db.refresh(new_chat)
	return schemas.GetChat.from_orm(new_chat)

# Load all chats in a room
async def load_chats(room_id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> List[schemas.GetChat]:
	# Room validation
	room_as_user_1 = db.query(models.RoomChatAgg).filter(models.RoomChatAgg.user_id_1==authenticated_user.id)
	room_as_user_2 = db.query(models.RoomChatAgg).filter(models.RoomChatAgg.user_id_2==authenticated_user.id)
	if not room_as_user_1.first() and not room_as_user_2.first():
		raise HTTPException(status_code=404, detail=f'You don\'t have any rooms for personal chat.')
	room_list = list(map(RoomSchemas.GetRoomChatAgg.from_orm, room_as_user_1)) + list(map(RoomSchemas.GetRoomChatAgg.from_orm, room_as_user_2))
	room_list = [int(dict(i)['room_id']) for i in room_list]
	if int(room_id) not in room_list:
		raise HTTPException(status_code=404, detail=f'Room with ID {room_id} not found.')
	# Get all chats
	chats = db.query(models.Chat).filter(models.Chat.room_id==room_id)
	if not chats.first():
		raise HTTPException(status_code=404, detail=f'There is no chat yet in this room.')
	return list(map(schemas.GetChat.from_orm, chats))

