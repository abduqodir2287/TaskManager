from redis import Redis

from src.domain.database.tasks.create_db import db
from src.config import settings


# При запуске проекта в Docker,
# Замените хост=settings.REDIS_HOST на хост=settings.DOCKER_REDIS_HOST.

class RedisClient:
	def __init__(self):
		self.redis_client = Redis(
			host=settings.REDIS_HOST, port=settings.REDIS_PORT,
			db=settings.REDIS_DATABASE, decode_responses="utf-8"
		)
		self.db = db

	def set_with_ttl(self, task_id: str | int, task_data: dict) -> None:
		self.redis_client.hset(task_id, mapping=task_data)
		self.redis_client.expire(task_id, settings.REDIS_CACHE_EXPIRATION)


	def set(self, name: str | int, data: str) -> None:
		self.redis_client.set(name, data)


	def get_dict(self, name: str | int) -> dict:
		if self.redis_client.exists(name):
			return self.redis_client.hgetall(name)

	def get(self, name: str | int) -> str:
		if self.redis_client.exists(name):
			return self.redis_client.get(name)

	def get_keys(self) -> list:
		return self.redis_client.keys("*")

	def delete(self, name: str | int) -> None:
		self.redis_client.delete(name)

	def exist(self, name: str | int) -> bool | None:
		if self.redis_client.exists(name):
			return True

