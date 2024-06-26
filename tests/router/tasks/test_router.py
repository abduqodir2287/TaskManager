from fastapi.testclient import TestClient

from src.main import app
from src.domain.tasks.schema import TaskStatus

client = TestClient(app)

def test_for_app():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"Message": "Hello World"}

def test_for_app_not_found():
	response = client.get("/something")
	assert response.status_code == 404
	assert response.json() == {"detail": "Not Found"}

def test_for_get_tasks():
	response = client.get("/Tasks")
	assert response.status_code == 200

def test_for_get_by_id_notfound():
	response = client.get("/Tasks/1243")
	assert response.status_code == 422
	assert response.json() == {"detail": "422: Task not found"}

def test_for_get_by_id_success():
	response = client.get("/Tasks/1")
	assert response.status_code == 200


def test_for_delete_task_notfound():
	response = client.get("/Tasks/123423421")
	assert response.status_code == 422
	assert response.json() == {"detail": "422: Task not found"}


def test_for_delete_task_success():
	response = client.get("/Tasks/1")
	assert response.status_code == 200


def test_for_update_task_success():
	response = client.get("/Tasks", params={
		"task_id": 1, "title": "Java",
		"description": "Programmer", "status": TaskStatus("completed")
	})
	assert response.status_code == 200

def test_for_update_task_notfound():
	response = client.get("/Tasks", params={
		"task_id": 12345, "title": "23142",
		"description": "sdgdfsg", "status": TaskStatus("completed")
	})
	assert response.status_code == 200
