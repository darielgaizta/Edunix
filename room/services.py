from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth import schemas as AuthSchemas
from user import models as UserModels

from . import models, schemas

# Create new empty room
async def create_room(name, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetRoom:
	new_room = models.Room(name=name)
	db.add(new_room)
	db.commit()
	
	# Return the newly created room
	db.refresh(new_room)
	return schemas.GetRoom.from_orm(new_room)

# Get all rooms for forum discussion
async def get_all_rooms(db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> List[schemas.GetRoom]:
	rooms = db.query(models.Room).filter(models.Room.name!=None)
	if not rooms.first():
		raise HTTPException(status_code=404, detail=f'There are no rooms yet for forum discussion.')
	return list(map(schemas.GetRoom.from_orm, rooms))

# Update room for forum discussion
async def update_room(id, request:schemas.Room, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	room = db.query(models.Room).filter(models.Room.id==id, models.Room.name!=None)
	if not room.first():
		raise HTTPException(status_code=404, detail=f'Room with ID {id} does not exists.')
	room.update(dict(request), synchronize_session=False)
	db.commit()

# Get all rooms for personal chat
async def get_all_room_chat(db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> List[schemas.GetRoomChatAgg]:
	room_as_user_1 = db.query(models.RoomChatAgg).filter(models.RoomChatAgg.user_id_1==authenticated_user.id)
	room_as_user_2 = db.query(models.RoomChatAgg).filter(models.RoomChatAgg.user_id_2==authenticated_user.id)
	if not room_as_user_1.first() and not room_as_user_2.first():
		raise HTTPException(status_code=404, detail=f'You don\'t have any rooms for personal chat.')
	return list(map(schemas.GetRoomChatAgg.from_orm, room_as_user_1)) + list(map(schemas.GetRoomChatAgg.from_orm, room_as_user_2))

# Create new room for personal chat
async def create_room_chat(to_user_id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetRoomChatAgg:
	to_user = db.query(UserModels.User).filter(UserModels.User.id==to_user_id)
	if not to_user.first():
		raise HTTPException(status_code=404, detail=f'User with ID {to_user_id} does not exists.')
	# Room validation
	room_as_user_1 = db.query(models.RoomChatAgg).filter(models.RoomChatAgg.user_id_1==authenticated_user.id, models.RoomChatAgg.user_id_2==to_user_id)
	room_as_user_2 = db.query(models.RoomChatAgg).filter(models.RoomChatAgg.user_id_2==authenticated_user.id, models.RoomChatAgg.user_id_1==to_user_id)
	if room_as_user_1.first() or room_as_user_2.first():
		raise HTTPException(status_code=404, detail=f'Room chat with user {to_user_id} is already exists.')
	# Create new personal room chat with the users
	new_room = models.Room(name=None)
	db.add(new_room)
	db.commit()
	db.refresh(new_room)
	new_room_chat_agg = models.RoomChatAgg(room_id=new_room.id, user_id_1=authenticated_user.id, user_id_2=to_user_id)
	db.add(new_room_chat_agg)
	db.commit()
	
	# Return the newly created room chat agg
	db.refresh(new_room_chat_agg)
	return schemas.GetRoomChatAgg.from_orm(new_room_chat_agg)

