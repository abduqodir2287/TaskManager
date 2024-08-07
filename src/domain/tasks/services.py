from typing import Optional
from fastapi import HTTPException, Query, status

from src.domain.tasks.schema import TasksModel, TaskStatus, TaskResponseForGet
from src.domain.tasks.schema import TaskResponse, TaskResponseForPut, AllTasks
from src.infrastructure.database.postgres.tasks.create_db import db
from src.infrastructure.database.redis.client import RedisClient
from src.domain.tasks.tasks_functions import TaskServiceFunctions
from src.configs.logger_setup import logger

class TaskRouterService(TaskServiceFunctions):
    def __init__(self) -> None:
        super().__init__()
        self.redis_client = RedisClient()
        self.logger = logger

    async def get_tasks_service(self) -> AllTasks:
        all_tasks = await self.get_all_task_redis_function()
        self.logger.info("Tasks sent successfully")

        return AllTasks(Tasks=all_tasks)

    async def get_task_by_id_service(self, task_id: int) -> TaskResponseForGet:
        try:
            task = await self.get_by_id_function(task_id)
            self.logger.info("Tasks sent successfully")

            return task

        except HTTPException as e:
            raise e

        except Exception as e:
            self.logger.error(f"The error is: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_task_service(self, task_id: int) -> None:
        try:
            delete = await db.delete_task_by_id(task_id)

            if delete is None:
                self.logger.warning("Task not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

            await self.delete_task_from_cache(task_id)
            self.logger.info("Task deleted successfully")

        except HTTPException as e:
            raise e

        except Exception as e:
            self.logger.error(f"The error is: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def add_task_service(
            self, title: str = Query(..., description="The title of the task"),
            description: Optional[str] = Query(None, description="The description of the task"),
            task_status: TaskStatus = Query(..., description="The status of the task")
    ) -> TaskResponse:
        try:
            task = TasksModel(
                title=title,
                description=description,
                status=task_status
            )

            insert_response = await db.insert_task(task)

            await self.add_task_in_cache(
                insert_response[0], title, description,
                task_status, insert_response[1],
                insert_response[2]
            )

            result = await self.add_id_service(insert_response[0], insert_response[1], task)
            self.logger.info("Task added successfully")
            return result

        except Exception as e:
            self.logger.error(f"The error is: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def update_task_service(
            self, task_id: int,
            title: Optional[str] = Query(None, description="The title of the task"),
            description: Optional[str] = Query(None, description="The description of the task"),
            task_status: Optional[TaskStatus] = Query(None, description="The status of the task")
    ) -> TaskResponseForPut:
        try:
            return await self.put_service_function(task_id, title, description, task_status)

        except HTTPException as e:
            raise e

        except Exception as e:
            self.logger.error(f"The error is: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
