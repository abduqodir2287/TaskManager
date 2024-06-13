from src.presentation.rest.routers import all_routers
from src.domain.tasks.task_app import app


for router in all_routers:
	app.include_router(router)
