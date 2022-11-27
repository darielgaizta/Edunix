from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from edunix import connection
from auth import schemas as AuthSchemas, services as AuthServices

from . import services, schemas, models

router = APIRouter(
	prefix='/note',
	tags=['Notes']
)

# Initialize tables
models.connection.Base.metadata.create_all(bind=connection.engine)

# Create note
@router.post('', status_code=201)
async def create_note(note:schemas.CreateNote, db:Session=Depends(connection.get_db), authenticated_user: AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.create_note(note=note, db=db, authenticated_user=authenticated_user)

# Get all notes
@router.get('', response_model=List[schemas.GetNote])
async def get_all_notes(db:Session=Depends(connection.get_db), authenticated_user: AuthSchemas.AuthenticatedUser=Depends(AuthServices.get_current_user)):
	return await services.get_all_notes(db=db, authenticated_user=authenticated_user)
