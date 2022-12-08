from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth import schemas as AuthSchemas

from . import models, schemas

EDUNIX_ADMIN = '18220009@std.stei.itb.ac.id'

# Create new
async def create_new(new:schemas.CreateNew, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetNew:
	if authenticated_user.email == EDUNIX_ADMIN:
		new_new = models.New(**new.dict())
		db.add(new_new)
		db.commit()
		# Return the newly created new
		db.refresh(new_new)
		return schemas.GetNew.from_orm(new_new)
	else:
		raise HTTPException(status_code=403, detail=f'You need permission to do this action.')

# Get all news
async def get_all_news(db:Session) -> List[schemas.GetNew]:
	news = db.query(models.New).all()
	return list(map(schemas.GetNew.from_orm, news))

# Get detail new
async def get_detail_new(id, db:Session) -> schemas.GetNew:
	new = db.query(models.New).filter(models.New.id == id).first()
	if not new:
		raise HTTPException(status_code=404, detail=f'News with ID {id} not found.')
	return schemas.GetNew.from_orm(new)

# Update new
async def update_new(id, request:schemas.New, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	if authenticated_user.email == EDUNIX_ADMIN:
		new = db.query(models.New).filter(models.New.id == id)
		if not new.first():
			raise HTTPException(status_code=404, detail=f'News with ID {id} not found.')
		# Add all attributes from request as dictionary -> JSON
		new.update(dict(request), synchronize_session=False)
		db.commit()
	else:
		raise HTTPException(status_code=403, detail=f'Forbidden access.')

# Delete new
async def destroy_new(id, db:Session, authenticated_user=AuthSchemas.AuthenticatedUser):
	if authenticated_user.email == EDUNIX_ADMIN:
		new = db.query(models.New).filter(models.New.id == id)
		if not new.first():
			raise HTTPException(status_code=404, detail=f'News with ID {id} not found.')
		new.delete(synchronize_session=False)
		db.commit()
	else:
		raise HTTPException(status_code=403, detail=f'Forbidden access.')