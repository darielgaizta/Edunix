from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
	username:str
	password:str
	email:str

# Get all attributes
class BaseUser(User):
	id:int
	date_created:datetime

	class Config:
		orm_mode = True

# Create user
class CreateUser(User):
	pass

	class Config:
		orm_mode = True

# Get user
class GetUser(BaseModel):
	username:str
	email:str

	class Config:
		orm_mode = True
