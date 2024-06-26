from datetime import datetime
from fastapi import HTTPException

from src.domain.tasks.schema import TasksModel, TasksModelForPut
from src.domain.database.tasks.create_db import db
from src.domain.redis_for_tasks.services import RedisClient

class ServiceFunctions:

	def __init__(self):
		self.redis_client = RedisClient()
		self.db = db

	async def add_id_service(self, id: int, created_at: datetime, task: TasksModel):
		return {
			"result": "Task added",
			"id": id,
			"title": task.title,
			"description": task.description,
			"status": task.status,
			"created_at": created_at
		}


	async def put_response_service(self, id: int, created_at: datetime, updated_at: datetime, task: TasksModelForPut):
		return {
			"result": "Task updated",
			"id": id,
			"title": task.title,
			"description": task.description,
			"status": task.status,
			"created_at": created_at,
			"updated_at": updated_at,
		}


	async def response_tasks_service(self):
		tasks = await self.db.select_all_tasks()
		tasks_list = []
		for task in tasks:
			all_tasks = {
				"id": task[0],
				"title": task[1],
				"description": task[2],
				"status": task[3],
				"created_at": task[4],
				"updated_at": task[5]
			}
			tasks_list.append(all_tasks)
		return tasks_list


	async def response_task_by_id_service(self, task_id: int) -> object:
		task = await self.redis_client.get(task_id)
		if task:
			print("Task from Cache")
			return task
		get_task = await self.db.select_task_by_id(task_id)
		if get_task is None:
			raise HTTPException(status_code=422, detail="Task not found")
		task_by_task_id = get_task[0]
		returned_task = {
			"id": task_by_task_id[0],
			"title": task_by_task_id[1],
			"description": task_by_task_id[2],
			"status": task_by_task_id[3],
			"created_at": task_by_task_id[4].isoformat(),
			"updated_at": task_by_task_id[5].isoformat()
		}
		await self.redis_client.set(task_id, returned_task)
		print("Task from Db")
		return returned_task
