from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth import schemas as AuthSchemas

from . import models, schemas

# Create note
async def create_note(note: schemas.CreateNote, db:Session, authenticated_user: AuthSchemas.AuthenticatedUser) -> schemas.GetNote:
	new_note = models.Note(**note.dict(), user_id=authenticated_user.id)
	db.add(new_note)
	db.commit()

	# Return the newly created note
	db.refresh(new_note)
	return schemas.GetNote.from_orm(new_note)

# Get all notes
async def get_all_notes(db: Session, authenticated_user: AuthSchemas.AuthenticatedUser) -> List[schemas.GetNote]:
	notes = db.query(models.Note).filter(models.Note.user_id==authenticated_user.id)
	if not notes.first():
		raise HTTPException(status_code=404, detail='You don\'t have any notes.')
	return list(map(schemas.GetNote.from_orm, notes))
