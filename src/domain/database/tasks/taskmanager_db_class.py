from sqlalchemy import MetaData, select, delete, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import settings
from src.domain.tasks.schema import TasksModel, TasksModelForPut
from src.domain.database.tasks.table import table

class TaskManagerDb:
	def __init__(self, table_name):
		self.table_name = table_name
		self.db_url = settings.DB_URL
		self.engine = create_async_engine(self.db_url)
		self.metadata = MetaData()
		self.tasks_table = table(self.metadata, self.table_name)

	async def create_table(self):
		async with self.engine.begin() as conn:
			await conn.run_sync(self.metadata.create_all)

	async def insert_task(self, task: TasksModel):
		async with AsyncSession(self.engine) as conn:
			async with conn.begin():
				insert_into = self.tasks_table.insert().values(
					title=task.title,
					description=task.description,
					status=task.status
				).returning(self.tasks_table.c.id, self.tasks_table.c.created_at)
				insert = await conn.execute(insert_into)
				row = insert.first()
				result = (row.id, row.created_at)
				return result

	async def select_all_tasks(self):
		async with AsyncSession(self.engine) as session:
			async with session.begin():
				select_tasks = select(self.tasks_table)
				all_tasks = await session.execute(select_tasks)
				return all_tasks.fetchall()

	async def delete_task_by_id(self, task_id: int):
		async with AsyncSession(self.engine) as session:
			async with session.begin():
				delete_task = delete(self.tasks_table).where(self.tasks_table.c.id == task_id)
				result = await session.execute(delete_task)
				if result.rowcount > 0:
					return True
				return None

	async def select_task_by_id(self, task_id: int):
		async with AsyncSession(self.engine) as session:
			async with session.begin():
				select_tasks = select(self.tasks_table).where(self.tasks_table.c.id == task_id)
				result = await session.execute(select_tasks)
				tasks = result.fetchall()
				if tasks:
					return tasks
				return None

	async def update_task_by_id(self, task_id: int, task: TasksModelForPut):
		async with AsyncSession(self.engine) as session:
			async with session.begin():
				update_task = update(self.tasks_table).where(self.tasks_table.c.id == task_id).values(
					title=task.title,
					description=task.description,
					status=task.status
				).returning(self.tasks_table.c.created_at, self.tasks_table.c.updated_at)

				result = await session.execute(update_task)
				row = result.first()
				if row:
					return {"created_at": row.created_at, "updated_at": row.updated_at}
				return None

