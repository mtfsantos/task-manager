from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.db.models import TaskStatusEnum
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services import task_service
from app.api.deps import get_db, get_current_user # Using mocked auth for now

router = APIRouter()

@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Authenticated
):
    """
    Create a new task.
    """
    db_task = task_service.create_task(db=db, task=task)
    return db_task

@router.get("/tasks", response_model=List[TaskOut])
def read_tasks(
    status: Optional[TaskStatusEnum] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Authenticated
):
    """
    Retrieve a list of tasks.
    Can filter by status (pending, in_progress, completed).
    """
    tasks = task_service.get_tasks(db=db, status=status)
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Authenticated
):
    """
    Retrieve a single task by its ID.
    """
    db_task = task_service.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: uuid.UUID,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Authenticated
):
    """
    Update an existing task's status or other details.
    """
    db_task = task_service.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Authenticated
):
    """
    Delete a task by its ID.
    """
    success = task_service.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
