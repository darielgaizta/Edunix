from pydantic import BaseModel
from datetime import datetime

class New(BaseModel):
	title:str
	content:str

# Get all attributes
class BaseNew(New):
	id:int
	date_published:datetime

# Create new schema
class CreateNew(New):
	pass

	class Config:
		orm_mode = True

# Get new schema
class GetNew(BaseNew):
	pass

	class Config:
		orm_mode = True