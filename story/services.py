from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth import schemas as AuthSchemas

from . import schemas, models

# Create story
async def create_story(story:schemas.CreateStory, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetStory:
	new_story = models.Story(**story.dict(), user_id=authenticated_user.id)
	db.add(new_story)
	db.commit()
	# Return the newly created story
	db.refresh(new_story)
	return schemas.GetStory.from_orm(new_story)

# Get all stories
async def get_all_stories(user_id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> List[schemas.GetStory]:
	stories = db.query(models.Story).filter(models.Story.user_id==user_id)
	if not stories.first():
		raise HTTPException(status_code=404, detail=f'User with ID {user_id} does not have any stories.')
	return list(map(schemas.GetStory.from_orm, stories))

# Get detail story
async def get_detail_story(user_id, id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetStory:
	story = db.query(models.Story).filter(models.Story.user_id==user_id, models.Story.id==id).first()
	if not story:
		raise HTTPException(status_code=404, detail=f'Story with ID {id} not found.')
	return schemas.GetStory.from_orm(story)

# Update story
async def update_story(user_id, id, request:schemas.CreateStory, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	if int(user_id) == int(authenticated_user.id):
		story = db.query(models.Story).filter(models.Story.user_id==authenticated_user.id, models.Story.id==id)
		if not story.first():
			raise HTTPException(status_code=404, detail=f'Story with ID {id} not found.')
		story.update(dict(request), synchronize_session=False)
		db.commit()
	else:
		raise HTTPException(status_code=403, detail=f'You need permission to do this action.')

# Delete story
async def destroy_story(user_id, id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	if int(user_id) == int(authenticated_user.id):
		story = db.query(models.Story).filter(models.Story.user_id==authenticated_user.id, models.Story.id==id)
		if not story.first():
			raise HTTPException(status_code=404, detail=f'Story with ID {id} not found.')
		story.delete(synchronize_session=False)
		db.commit()
	else:
		raise HTTPException(status_code=403, detail=f'You need permission to do this action.')