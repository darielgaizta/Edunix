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

# Get detail note
async def get_detail_note(id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetNote:
	note = db.query(models.Note).filter(models.Note.user_id==authenticated_user.id, models.Note.id==id).first()
	if not note:
		raise HTTPException(status_code=404, detail='Note with ID {id} not found.')
	return schemas.GetNote.from_orm(note)

# Update note
async def update_note(id, request:schemas.Note, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	note = db.query(models.Note).filter(models.Note.user_id==authenticated_user.id, models.Note.id==id)
	if not note.first():
		raise HTTPException(status_code=404, detail='Note with ID {id} not found.')
	note.update(dict(request), synchronize_session=False)
	db.commit()

# Delete note
async def destroy_note(id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	note = db.query(models.Note).filter(models.Note.user_id==authenticated_user.id, models.Note.id==id)
	if not note.first():
		raise HTTPException(status_code=404, detail='Note with ID {id} not found.')
	note.delete(synchronize_session=False)
	db.commit()

# Set public status: share note
async def set_public_status(id, request:schemas.SetPublicNote, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser):
	note = db.query(models.Note).filter(models.Note.user_id==authenticated_user.id, models.Note.id==id)
	if not note.first():
		raise HTTPException(status_code=404, detail='Note with ID {id} not found.')
	note.update(dict(request), synchronize_session=False)
	db.commit()

# Get detail public note
async def get_detail_public_note(id, db:Session, authenticated_user:AuthSchemas.AuthenticatedUser) -> schemas.GetNote:
	note = db.query(models.Note).filter(models.Note.is_public==True, models.Note.id==id).first()
	if not note:
		raise HTTPException(status_code=404, detail='Note with ID {id} not found.')
	return schemas.GetNote.from_orm(note)

# Get all public notes from particular user
async def get_all_public_notes(user_id, db: Session, authenticated_user: AuthSchemas.AuthenticatedUser) -> List[schemas.GetNote]:
	notes = db.query(models.Note).filter(models.Note.user_id==user_id, models.Note.is_public==True)
	if not notes.first():
		raise HTTPException(status_code=404, detail='You don\'t have any notes.')
	return list(map(schemas.GetNote.from_orm, notes))