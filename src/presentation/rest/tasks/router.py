from typing import Optional
from fastapi import APIRouter, status, Query

from src.domain.tasks.schema import AllTasks, TaskResponseForGet, TaskStatus, TaskResponse, TaskResponseForPut
from src.domain.tasks.services import TaskRouterService

router = APIRouter(prefix="/Tasks", tags=["Task"])

service = TaskRouterService()


@router.get("", response_model=AllTasks, status_code=status.HTTP_200_OK)
async def get_task() -> AllTasks:
	return await service.get_tasks_service()


@router.get("/{task_id}", response_model=TaskResponseForGet, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int) -> TaskResponseForGet:
	return await service.get_task_by_id_service(task_id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int) -> None:
	return await service.delete_task_service(task_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def add_task(
    title: str = Query(..., description="The title of the task"),
    description: Optional[str] = Query(None, description="The description of the task"),
    task_status: TaskStatus = Query(..., description="The status of the task")
) -> TaskResponse:
	return await service.add_task_service(title, description, task_status)

@router.put("/{task_id}", response_model=TaskResponseForPut, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    title: Optional[str] = Query(default=None, description="The title of the task"),
    description: Optional[str] = Query(default=None, description="The description of the task"),
    task_status: TaskStatus = Query(default=None, description="The status of the task")
) -> TaskResponseForPut:
	return await service.update_task_service(task_id, title, description, task_status)
