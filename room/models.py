from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from edunix import connection

class Room(connection.Base):
	__tablename__ = 'rooms'

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True, default=None, nullable=True)

	# Relationships
	room_chat = relationship('RoomChatAgg', back_populates='room')
	all_chats = relationship('Chat', back_populates='in_room')

class RoomChatAgg(connection.Base):
	__tablename__ = 'room_chat_agg'

	id = Column(Integer, primary_key=True)

	# Foreign Keys
	room_id = Column(Integer, ForeignKey('rooms.id'))
	user_id_1 = Column(Integer, ForeignKey('users.id'))
	user_id_2 = Column(Integer, ForeignKey('users.id'))

	# Relationships
	room = relationship('Room', back_populates='room_chat')
	user_1 = relationship('User', back_populates='as_user_1', foreign_keys=[user_id_1])
	user_2 = relationship('User', back_populates='as_user_2', foreign_keys=[user_id_2])