1. из `main.py` сделать стартовый файл, который запускает весь проект(убрать запуск из src/domain/tasks/task_app.py) -> ✅
2. почитать про миграции(https://habr.com/ru/companies/yandex/articles/511892/), использовать `alembic` для их прогона
3. изменить наименования `make` команд,ruff -> lint, run -> todo-run, todo-stop -> ✅
4. добавить hot-reload приложению в docker-compose, который будет следить за изменениями в проекте, ex: https://stackoverflow.com/questions/69460295/how-to-enable-live-reload-in-a-dockerised-fastapi-application-using-docker-compo -> ✅
5. использовать один environment для POSTGRES, избавиться от POSTGRES_HOST и POSTGRES_DOCKER_HOST -> ✅
6. Вынести работу с БД в отдельный слой: src/infrastructure/database/redis | postgres -> client -> ✅
7. Annotation repeat:
    ```python
        async def get_tasks_service(self) -> AllTasks:
            all_tasks = await self.functions.get_all_task_redis_function()
            self.logger.info("Tasks submitted successfully")
            return AllTasks(Tasks=all_tasks)
    ```  -> ✅
