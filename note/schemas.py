from pydantic import BaseModel
from datetime import datetime


class Note(BaseModel):
	title:str
	content:str

# Get all attributes
class BaseNote(Note):
	id:int
	user_id:int
	is_public:bool
	date_created:datetime

# Create note schema
class CreateNote(Note):
	pass

	class Config:
		orm_mode = True

# Get Note schema
class GetNote(BaseNote):
	pass

	class Config:
		orm_mode = True

class SetPublicNote(BaseModel):
	is_public:bool