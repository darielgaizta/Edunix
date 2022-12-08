from typing import List
from sqlalchemy.orm import Session
from auth.services import Hash

from . import models, schemas

# Create user
async def create_user(user:schemas.CreateUser, db:Session) -> schemas.GetUser:
	user.password = Hash.encrypt(user.password)
	new_user = models.User(**user.dict())
	db.add(new_user)
	db.commit()
	# Return the newly created user
	db.refresh(new_user)
	return schemas.GetUser.from_orm(new_user)

# Get all user
async def get_all_users(db:Session) -> List[schemas.GetUser]:
	users = db.query(models.User).all()
	return list(map(schemas.GetUser.from_orm, users))

	