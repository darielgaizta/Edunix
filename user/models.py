from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from edunix import connection

class User(connection.Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True)
	password = Column(String, index=True)
	email = Column(String, index=True, unique=True)
	date_created = Column(DateTime, default=datetime.utcnow)

	# Relationships
	notes = relationship('Note', back_populates='writer')
