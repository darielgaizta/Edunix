from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from edunix import connection

# Import relations
from user.models import User

class Story(connection.Base):
	__tablename__ = 'stories'

	id = Column(Integer, primary_key=True, index=True)
	content = Column(String, index=True)
	date_created = Column(DateTime, index=True, default=datetime.utcnow)

	# Foreign keys
	user_id = Column(Integer, ForeignKey('users.id'))

	# Relationships
	teller = relationship('User', back_populates='stories')