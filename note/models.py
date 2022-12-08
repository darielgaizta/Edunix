from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from edunix import connection

# Import relations
from user.models import User

class Note(connection.Base):
	__tablename__ = 'notes'

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	content = Column(String)
	is_public = Column(Boolean, default=False)
	date_created = Column(DateTime, default=datetime.utcnow)

	# Foreign keys
	user_id = Column(Integer, ForeignKey('users.id'))

	# Relationships
	writer = relationship('User', back_populates='notes')
