from fastapi import FastAPI, status
from src.domain.database.tasks.create_db import db
from src.domain.tasks.schema import GreetingsResponse

app = FastAPI()


@app.on_event("startup")
async def startup_event():
	await db.create_table()


@app.get("/", response_model=GreetingsResponse, status_code=status.HTTP_200_OK)
async def hello():
	return {"Message": "Hello World"}
