from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Task, TaskStatusEnum
from app.schemas.task import TaskCreate, TaskUpdate

def create_task(db: Session, task: TaskCreate):
    """
    Creates a new task in the database.
    """
    db_task = Task(**task.model_dump()) # Use model_dump() for Pydantic v2
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    """
    Retrieves a single task by its ID.
    """
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, status: Optional[TaskStatusEnum] = None, skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Retrieves a list of tasks, with optional filtering by status.
    """
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task: TaskUpdate):
    """
    Updates an existing task.
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        update_data = task.model_dump(exclude_unset=True) # Use model_dump() for Pydantic v2
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """
    Deletes a task by its ID.
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
