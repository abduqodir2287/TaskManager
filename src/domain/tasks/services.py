from datetime import datetime
from typing import Optional
from fastapi import HTTPException, Query

from src.domain.tasks.schema import TasksModel, TaskStatus
from src.domain.database.tasks.create_db import db

class TaskRouterService:

    async def get_tasks_service(self):
        all_tasks = await self.response_tasks_service()
        return {"Tasks": all_tasks}

    async def get_task_by_id_service(self, task_id: int):
        try:
            task = await self.response_task_by_id_service(task_id)
            if task is None:
                raise HTTPException(status_code=422, detail="Task not found")
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
            result = await self.add_id_service(insert_response[0], insert_response[1], task)
            return result
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))


    async def update_task_service(
            self, task_id: int,
            title: str = Query(..., description="The title of the task"),
            description: Optional[str] = Query(None, description="The description of the task"),
            task_status: TaskStatus = Query(..., description="The status of the task")
    ):
        try:
            task = TasksModel(
                title=title,
                description=description,
                status=task_status
            )
            update = await db.update_task_by_id(task_id, task)
            if update is None:
                raise HTTPException(status_code=422, detail="Task not found")
            result = await self.put_response_service(task_id, update["created_at"], update["updated_at"], task)
            return result
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))


    async def add_id_service(self, id: int, created_at: datetime, task: TasksModel):
        return {
            "result": "Task added",
            "id": id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": created_at
        }

    async def put_response_service(self, id: int, created_at: datetime, updated_at: datetime, task: TasksModel):
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
        tasks = await db.select_all_tasks()
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
        task = await db.select_task_by_id(task_id)
        if task is None:
            return None
        for task_by_task_id in task:
            returned_task = {
                "id": task_by_task_id[0],
                "title": task_by_task_id[1],
                "description": task_by_task_id[2],
                "status": task_by_task_id[3],
                "created_at": task_by_task_id[4],
                "updated_at": task_by_task_id[5],
            }
            return returned_task

