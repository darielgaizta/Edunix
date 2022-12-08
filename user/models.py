from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from edunix import connection

# Import relations
from room.models import RoomChatAgg

class User(connection.Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True)
	password = Column(String, index=True)
	email = Column(String, index=True, unique=True)
	date_created = Column(DateTime, default=datetime.utcnow)

	# Relationships
	notes = relationship('Note', back_populates='writer')
	stories = relationship('Story', back_populates='teller')
	as_user_1 = relationship('RoomChatAgg', back_populates='user_1', foreign_keys=[RoomChatAgg.user_id_1])
	as_user_2 = relationship('RoomChatAgg', back_populates='user_2', foreign_keys=[RoomChatAgg.user_id_2])
	chats = relationship('Chat', back_populates='sender')