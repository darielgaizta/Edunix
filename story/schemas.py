from pydantic import BaseModel
from datetime import datetime

class Story(BaseModel):
	content:str
	date_created:datetime

# Get all attributes
class BaseStory(Story):
	id:int
	user_id:int

# Create story schema
class CreateStory(BaseModel):
	content:str

# Get story schema
class GetStory(BaseStory):
	pass

	class Config:
		orm_mode = True
