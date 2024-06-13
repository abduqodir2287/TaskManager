test_run:
	python main.py

run:
	uvicorn src.main:app --reload --port 8012

req:
	pip freeze > requirements.txt

test:
	python -m pytest

doc:
	docker-compose up --build

git:
	git status