from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import json

from src.domain.tasks.schema import TaskResponse, TaskStatus, TaskResponseForPut
from src.domain.tasks.schema import TasksModel, TasksModelForPut, TaskResponseForGet
from src.infrastructure.database.postgres.tasks.create_db import db
from src.configs.logger_setup import logger
from src.infrastructure.database.redis.client import RedisClient


class TaskServiceFunctions:

	def __init__(self):
		self.redis_client = RedisClient()
		self.db = db
		self.logger = logger

	async def add_id_service(self, id: int, created_at: datetime, task: TasksModel) -> TaskResponse:
		return TaskResponse(
			result="Task added",
			id=id,
			title=task.title,
			description=task.description,
			status=task.status,
			created_at=created_at
		)

	async def add_task_in_cache(
			self, task_id: int, title: str, description: str,
			task_status: TaskStatus, created_at: datetime, updated_at: datetime
	) -> None:
		task = TaskResponseForGet(
			id=task_id,
			title=title,
			description=description,
			status=task_status,
			created_at=created_at,
			updated_at=updated_at
		)

		self.logger.info("Task added to Redis")
		self.redis_client.set(task_id, json.dumps(jsonable_encoder(task)))

	async def update_response_function(
			self, id: int, created_at: datetime,
			updated_at: datetime, task: TasksModelForPut
	) -> TaskResponseForPut:
		return TaskResponseForPut(
			result="Task updated",
			id=id,
			title=task.title,
			description=task.description,
			status=task.status,
			created_at=created_at,
			updated_at=updated_at,
		)

	async def put_service_function(
			self, task_id: int, title: Optional[str],
			description: Optional[str], task_status: Optional[TaskStatus]
	) -> TaskResponseForPut:
		task_by_id = await db.select_task_by_id(task_id)
		if task_by_id is None:
			self.logger.warning("Task not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

		task = TasksModelForPut(
			title=title if title is not None else task_by_id.title,
			description=description if description is not None else task_by_id.description,
			status=task_status if task_status is not None else task_by_id.status
		)

		update = await self.db.update_task_by_id(task_id, task)
		result = await self.update_response_function(
			task_id, update["created_at"],
			update["updated_at"], task
		)
		await self.update_task_in_cache(task_id, task, update["created_at"], update["updated_at"])
		self.logger.info("Task updated")

		return result


	async def update_task_in_cache(
			self, task_id: int, task: TasksModelForPut,
			created_at: datetime, updated_at: datetime
	) -> None:
		result = await self.update_response_function(
			task_id, created_at,
			updated_at, task
		)

		result_cache = jsonable_encoder(result)
		result_cache.pop("result", "Task updated")
		self.redis_client.set(task_id, json.dumps(result_cache))
		self.logger.info("Task updated to Redis")


	async def get_all_task_function(self) -> list:
		keys = self.redis_client.get_keys()
		tasks_list = []

		for key in keys:
			returned_task = self.redis_client.get(key)
			tasks_list.append(json.loads(returned_task))

		return tasks_list

	async def get_by_id_function(self, task_id: int) -> TaskResponseForGet:
		task = self.redis_client.get(task_id)
		if task:
			return json.loads(task)

		task_by_id = await self.db.select_task_by_id(task_id)
		if task_by_id is None:
			self.logger.warning("Task not found")
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

		returned_task = TaskResponseForGet(
			id=task_by_id[0],
			title=task_by_id[1],
			description=task_by_id[2],
			status=task_by_id[3],
			created_at=task_by_id[4].isoformat(),
			updated_at=task_by_id[5].isoformat()
		)

		self.redis_client.set(task_id, json.dumps(jsonable_encoder(returned_task)))

		return returned_task

	async def delete_task_from_cache(self, task_id: int) -> bool | None:
		if self.redis_client.exist(task_id):
			self.redis_client.delete(task_id)
			self.logger.info("Task deleted from Redis")
			return True

