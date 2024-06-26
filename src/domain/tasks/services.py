from typing import Optional
from fastapi import HTTPException, Query

from src.domain.tasks.schema import TasksModel, TaskStatus, TasksModelForPut
from src.domain.database.tasks.create_db import db
from src.domain.redis_for_tasks.services import RedisClient
from src.domain.tasks.tasks_functions import ServiceFunctions

class TaskRouterService:
    def __init__(self):
        self.redis_client = RedisClient()
        self.functions = ServiceFunctions()

    async def get_tasks_service(self):
        all_tasks = await self.functions.response_tasks_service()
        return {"Tasks": all_tasks}

    async def get_task_by_id_service(self, task_id: int):
        try:
            task = await self.functions.response_task_by_id_service(task_id)
            return task
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

    async def delete_task_service(self, task_id: int):
        try:
            delete = await db.delete_task_by_id(task_id)
            if delete is None:
                raise HTTPException(status_code=422, detail="Task not found")
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

    async def add_task_service(
            self, title: str = Query(..., description="The title of the task"),
            description: Optional[str] = Query(None, description="The description of the task"),
            task_status: TaskStatus = Query(..., description="The status of the task")
    ):
        try:
            task = TasksModel(
                title=title,
                description=description,
                status=task_status
            )
            insert_response = await db.insert_task(task)
            result = await self.functions.add_id_service(insert_response[0], insert_response[1], task)
            return result
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))


    async def update_task_service(
            self, task_id: int,
            title: Optional[str] = Query(None, description="The title of the task"),
            description: Optional[str] = Query(None, description="The description of the task"),
            task_status: Optional[TaskStatus] = Query(None, description="The status of the task")
    ):
        try:
            task_by_id = await db.select_task_by_id(task_id)
            if task_by_id is None:
                raise HTTPException(status_code=422, detail="Task not found")
            for existing_task in task_by_id:
                task = TasksModelForPut(
                    title=title if title is not None else existing_task.title,
                    description=description if description is not None else existing_task.description,
                    status=task_status if task_status is not None else existing_task.status
                )
                update = await db.update_task_by_id(task_id, task)
                result = await self.functions.put_response_service(
                    task_id, update["created_at"],
                    update["updated_at"], task
                )
                return result
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

