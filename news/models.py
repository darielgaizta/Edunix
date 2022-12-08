from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from edunix import connection

# News for Edunix Square
class New(connection.Base):
	__tablename__ = 'news'

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	content = Column(String)
	date_published = Column(DateTime, default=datetime.utcnow)
