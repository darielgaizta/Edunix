from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from edunix import connection

# Import relations
from user.models import User
from room.models import Room, RoomChatAgg

class Chat(connection.Base):
	__tablename__ = 'chats'
	
	id = Column(Integer, primary_key=True, index=True)
	text = Column(String)
	date_sent = Column(DateTime, default=datetime.utcnow)

	# Foreign keys
	user_id = Column(Integer, ForeignKey('users.id'))
	room_id = Column(Integer, ForeignKey('rooms.id'))

	# Relationships
	sender = relationship('User', back_populates='chats')
	in_room = relationship('Room', back_populates='all_chats')