from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in progress"
    completed = "completed"

class TasksModel(BaseModel):
    title: str = Field(description="The title of the task")
    description: Optional[str] = Field(default=None, description="The description of the task")
    status: TaskStatus = Field(description="The status of the task")


class TaskResponse(BaseModel):
    result: str
    id: int = Field(description="The id of the task")
    title: str = Field(description="The title of the task")
    description: Optional[str] = Field(default=None, description="The description of the task")
    status: TaskStatus = Field(description="The status of the task")
    created_at: datetime = Field(description="The creation datetime of the task")

class TaskResponseForPut(BaseModel):
    result: str
    id: int = Field(description="The id of the task")
    title: str = Field(description="The title of the task")
    description: Optional[str] = Field(default=None, description="The description of the task")
    status: TaskStatus = Field(description="The status of the task")
    created_at: datetime = Field(description="The creation datetime of the task")
    updated_at: datetime = Field(description="The last updated datetime of the task")


class GreetingsResponse(BaseModel):
    Message: str = Field(description="Any Message example ('Hello World')")

class TaskResponseForGet(BaseModel):
    id: int = Field(description="The id of the task")
    title: str = Field(description="The title of the task")
    description: Optional[str] = Field(default=None, description="The description of the task")
    status: TaskStatus = Field(description="The status of the task")
    created_at: datetime = Field(description="The creation datetime of the task")
    updated_at: datetime = Field(description="The last updated datetime of the task")

class AllTasks(BaseModel):
    Tasks: list[TaskResponseForGet]
