from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from edunix import connection
from auth import schemas as AuthSchemas, services as AuthServices

from . import services, schemas, models

router = APIRouter(
	prefix='/story',
	tags=['Stories']
)

# Initialize tables
models.connection.Base.metadata.create_all(bind=connection.engine)

# Create story
@router.post('', status_code=201)
async def create_story(story:schemas.CreateStory, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)) -> schemas.GetStory:
	return await services.create_story(story=story, db=db, authenticated_user=authenticated_user)

# Get all stories
@router.get('/{user_id}', response_model=List[schemas.GetStory])
async def get_all_stories(user_id, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)) -> List[schemas.GetStory]:
	return await services.get_all_stories(user_id=user_id, db=db, authenticated_user=authenticated_user)

# Get detail stories
@router.get('/{user_id}/{id}', response_model=schemas.GetStory)
async def get_detail_story(user_id, id, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)) -> schemas.GetStory:
	return await services.get_detail_story(user_id=user_id, id=id, db=db, authenticated_user=authenticated_user)

# Update story
@router.put('/{user_id}/{id}', status_code=204)
async def update_story(user_id, id, request:schemas.CreateStory, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.update_story(user_id=user_id, id=id, request=request, db=db, authenticated_user=authenticated_user)

# Delete story
@router.delete('/{user_id}/{id}', status_code=204)
async def destroy_story(user_id, id, db:Session=Depends(connection.get_db), authenticated_user:AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.destroy_story(user_id=user_id, id=id, db=db, authenticated_user=authenticated_user)