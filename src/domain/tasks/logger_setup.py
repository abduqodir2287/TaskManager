import logging
from src.config import settings

logger = logging.getLogger("Tasks")
logger.setLevel(level=logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filehandler = logging.FileHandler(f"tasks_log.log", mode='w')
filehandler.setFormatter(formatter)

if settings.LOG_WRITE_STATUS:
	logger.addHandler(filehandler)

handler.setFormatter(formatter)
logger.addHandler(handler)
