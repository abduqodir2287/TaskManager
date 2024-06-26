run:
	uvicorn src.main:app --reload --port 8000

req:
	pip freeze > requirements.txt

test:
	python -m pytest

up:
	docker-compose up --build

down:
	docker-compose down

git:
	git status

cli:
	redis-cli
