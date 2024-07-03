todo-run:
	uvicorn src.main:app --reload --port 8004

test:
	python -m pytest

up:
	docker-compose up -d --build

down:
	docker-compose down

linet:
	ruff check --fix
