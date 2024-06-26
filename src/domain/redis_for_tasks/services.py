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

	async def set(self, task_id, task_data):
		if self.redis_client.hset(task_id, mapping=task_data):
			self.redis_client.expire(task_id, settings.REDIS_CACHE_EXPIRATION)
			return True

	async def get(self, task_id):
		if self.redis_client.exists(task_id):
			return self.redis_client.hgetall(task_id)


	async def delete(self, task_id):
		if self.redis_client.delete(task_id):
			return True

