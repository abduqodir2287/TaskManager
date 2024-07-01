1. Статусы ошибок -> ✅
2. Обновлять данные при `POST/PATCH` методах -> ✅
3. Сериализация данных при добавлении/удалении данных из `Redis` пример(`json.dumps()` и `json.loads()`) -> ✅
4. https://habr.com/ru/articles/800413/ почитать про Аннотацию типов и попробовать использовать в проекте пример -> ✅
   ```
     def set_with_ttl(self, task_id, task_data) -> None:
         self.redis_client.hset(task_id, mapping=task_data)
         self.redis_client.expire(task_id, settings.REDIS_CACHE_EXPIRATION)
   ```
   Где None означает что функция ничего не возвращает

5. Почитать про линеты и зачем они нужны. Добавить `линет` в проект, пример: `ruff` https://docs.astral.sh/ruff/ -> ✅
6. Добавить логгирование, почитать про уровни логгирования https://habr.com/ru/companies/wunderfund/articles/683880/
7. Почитать про чистую архитектуру https://habr.com/ru/companies/otus/articles/732178/
8. Вместо `SQLite` использовать `PostgreSQL`
9. Почистить код от мусора, комментариев и от неиспользуемых блоков кода -> ✅
10. Визуально разделить блоки кода -> ✅