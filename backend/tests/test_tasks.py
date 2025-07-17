import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.models import TaskStatusEnum 

def test_login_failure(client: TestClient):
    response = client.post(
        "/api/v1/login",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    
def test_login_success(client: TestClient, test_user_credentials):
    response = client.post(
        "/api/v1/login",
        data={
            "username": test_user_credentials["username"],
            "password": test_user_credentials["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_task(client: TestClient, auth_token: str):
    response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Task", "description": "This is a test task.", "status": "pending"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_read_tasks(client: TestClient, auth_token: str, db_session: Session):
    client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Task 1", "status": "pending"}
    )
    client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Task 2", "status": "completed"}
    )

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2 
    assert any(task["title"] == "Task 1" for task in data)
    assert any(task["title"] == "Task 2" for task in data)

def test_read_tasks_filter_by_status(client: TestClient, auth_token: str, db_session: Session):
    client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Pending Task", "status": "pending"}
    )
    client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Completed Task", "status": "completed"}
    )

    response = client.get(
        "/api/v1/tasks?status=pending",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Pending Task"
    assert data[0]["status"] == "pending"

def test_read_single_task(client: TestClient, auth_token: str, db_session: Session):
    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Single Task", "status": "pending"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Task"
    assert data["id"] == task_id

def test_read_nonexistent_task(client: TestClient, auth_token: str):
    response = client.get(
        "/api/v1/tasks/99999999-9999-9999-9999-999999999999", 
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task(client: TestClient, auth_token: str, db_session: Session):
    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Task to Update", "description": "Original description", "status": "pending"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"status": "completed", "description": "Updated description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task to Update" 
    assert data["status"] == "completed"
    assert data["description"] == "Updated description"

def test_update_nonexistent_task(client: TestClient, auth_token: str):
    response = client.put(
        "/api/v1/tasks/99999999-9999-9999-9999-999999999999",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"status": "completed"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task(client: TestClient, auth_token: str, db_session: Session):
    create_response = client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Task to Delete", "status": "pending"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204 

    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404

def test_delete_nonexistent_task(client: TestClient, auth_token: str):
    response = client.delete(
        "/api/v1/tasks/99999999-9999-9999-9999-999999999999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_unauthenticated_access_to_tasks(client: TestClient):
    response = client.get("/api/v1/tasks") 
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
