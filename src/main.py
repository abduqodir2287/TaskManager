from src.presentation.rest.routers import all_routers
from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from src.infrastructure.database.postgres.tasks.create_db import db
from src.domain.tasks.schema import GreetingsResponse


@asynccontextmanager
async def lifespan_app(my_app: FastAPI):
	await db.create_table()
	yield


app = FastAPI(lifespan=lifespan_app)


@app.get("/", response_model=GreetingsResponse, status_code=status.HTTP_200_OK)
async def hello():
	return {"Message": "Hello World"}


for router in all_routers:
	app.include_router(router)

