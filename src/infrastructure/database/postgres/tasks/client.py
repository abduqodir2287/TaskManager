from sqlalchemy import select, delete, update

from src.configs.config import settings
from src.domain.tasks.schema import TasksModel, TasksModelForPut
from src.infrastructure.database.postgres.tasks.models import TaskManager
from src.infrastructure.database.postgres.tasks.database import Base, engine, async_session
from src.configs.logger_setup import logger

class TaskManagerDb:
	def __init__(self):
		self.db_url = settings.DATABASE_URL
		self.engine = engine
		self.metadata = Base.metadata
		self.async_session = async_session


	async def create_table(self) -> None:
		async with self.engine.begin() as conn:
			await conn.run_sync(self.metadata.create_all)


	async def insert_task(self, task: TasksModel) -> tuple:
		async with self.async_session() as session:
			async with session.begin():
				insert_into = TaskManager(
					title=task.title,
					description=task.description,
					status=task.status
				)
				session.add(insert_into)
			await session.commit()

			await session.refresh(insert_into)
			result = (insert_into.id, insert_into.created_at, insert_into.updated_at)

			logger.info("Task added to DB")
			return result


	async def select_all_tasks(self) -> list:
		async with self.async_session() as session:
			select_tasks = select(TaskManager)

			result = await session.execute(select_tasks)

			return result.scalars().all()


	async def delete_task_by_id(self, task_id: int) -> bool | None:
		async with self.async_session() as session:
			async with session.begin():

				delete_task = delete(TaskManager).where(TaskManager.id == task_id)
				result = await session.execute(delete_task)

				await session.commit()

				if result.rowcount > 0:
					return True


	async def select_task_by_id(self, task_id: int) -> TaskManager:
		async with self.async_session() as session:
			result = await session.execute(select(TaskManager).where(TaskManager.id == task_id))
			task = result.scalars().first()

			if task:
				return task


	async def update_task_by_id(self, task_id: int, task: TasksModelForPut) -> dict | None:
		async with self.async_session() as session:
			async with session.begin():
				update_task = update(TaskManager).where(TaskManager.id == task_id).values(
					title=task.title,
					description=task.description,
					status=task.status
				).returning(TaskManager.created_at, TaskManager.updated_at)

				result = await session.execute(update_task)
				await session.commit()

				row = result.fetchone()

				if row:
					return {"created_at": row.created_at, "updated_at": row.updated_at}

