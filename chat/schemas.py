from pydantic import BaseModel
from datetime import datetime

class Chat(BaseModel):
	text:str

class BaseChat(Chat):
	id:int
	user_id:int
	room_id:int
	date_sent:datetime

class CreateChat(Chat):
	pass

	class Config:
		orm_mode = True

class GetChat(BaseChat):
	pass

	class Config:
		orm_mode = True
