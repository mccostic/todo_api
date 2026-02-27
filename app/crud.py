from sqlalchemy.orm import Session
from . import models, schemas
from .core.exceptions import TodoNotFoundException
import uuid

def get_todos(db: Session):
    return db.query(models.Todo).order_by(
        models.Todo.created_at.desc()
    ).all()

def get_todo(db: Session, todo_id: str):
    return db.query(models.Todo).filter(
        models.Todo.id == todo_id
    ).first()

def get_todo_or_raise(db: Session, todo_id: str):
    todo = get_todo(db, todo_id)
    if not todo:
        raise TodoNotFoundException(
            details=f"Todo with id '{todo_id}' not found"
        )
    return todo

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(
        id=str(uuid.uuid4()),
        title=todo.title,
        description=todo.description,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: str, todo: schemas.TodoUpdate):
    db_todo = get_todo_or_raise(db, todo_id)

    update_data = todo.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: str):
    db_todo = get_todo_or_raise(db, todo_id)
    db.delete(db_todo)
    db.commit()

def toggle_todo(db: Session, todo_id: str):
    db_todo = get_todo_or_raise(db, todo_id)
    db_todo.is_completed = not db_todo.is_completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo_count(db: Session) -> int:
    return db.query(models.Todo).count()