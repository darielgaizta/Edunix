from typing import Optional
from pydantic import BaseModel

# Room
class Room(BaseModel):
	name:Optional[str]

class BaseRoom(Room):
	id:int

class GetRoom(BaseRoom):
	pass

	class Config:
		orm_mode = True

# Room Chat Agg
class RoomChatAgg(BaseModel):
	room_id:int
	user_id_1:int
	user_id_2:int

class CreateRoomChatAgg(BaseModel):
	user_id_1:int
	user_id_2:int

class ViewRoomChatAgg(CreateRoomChatAgg):
	pass
	
	class Config:
		orm_mode = True

class GetRoomChatAgg(RoomChatAgg):
	pass

	class Config:
		orm_mode = True