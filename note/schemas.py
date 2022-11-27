from pydantic import BaseModel
from datetime import datetime


class Note(BaseModel):
	title:str
	content:str

# Get all attributes
class BaseNote(Note):
	id:int
	user_id:int
	date_created:datetime

	class Config:
		orm_mode = True

# Create note schema
class CreateNote(Note):
	pass

	class Config:
		orm_mode = True

# Get Note schema
class GetNote(Note):
	date_created:datetime

	class Config:
		orm_mode = True
