from sqlalchemy import Column, Integer, Text, TIMESTAMP, func

from src.infrastructure.database.postgres.tasks.database import Base


class TaskManager(Base):
	__tablename__ = "tasks_table"

	id = Column(Integer, primary_key=True)
	title = Column(Text)
	description = Column(Text)
	status = Column(Text)
	created_at = Column(TIMESTAMP, server_default=func.now())
	updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

