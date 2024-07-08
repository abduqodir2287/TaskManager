start-todo:
	uvicorn src.main:app --reload --port 8000

test:
	python -m pytest

up:
	docker-compose up -d --build

down:
	docker-compose down

lint:
	ruff check --fix

upgrade:
	python -m alembic upgrade head
