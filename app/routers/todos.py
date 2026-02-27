from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..core.dependencies import verify_api_key
from ..core.exceptions import (
    TodoTitleEmptyException,
    TodoLimitExceededException,
)
from .. import crud, schemas

MAX_TODOS = 100

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(verify_api_key)],
)

@router.get(
    "/",
    response_model=List[schemas.TodoResponse],
    summary="Get all todos",
)
def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@router.get(
    "/{todo_id}",
    response_model=schemas.TodoResponse,
    summary="Get a single todo",
)
def get_todo(todo_id: str, db: Session = Depends(get_db)):
    # get_todo_or_raise handles 404 automatically
    return crud.get_todo_or_raise(db, todo_id)

@router.post(
    "/",
    response_model=schemas.TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    # Check business limit
    count = crud.get_todo_count(db)
    if count >= MAX_TODOS:
        raise TodoLimitExceededException(
            details=f"Maximum of {MAX_TODOS} todos allowed. Current count: {count}",
        )

    return crud.create_todo(db, todo)

@router.put(
    "/{todo_id}",
    response_model=schemas.TodoResponse,
    summary="Update a todo",
)
def update_todo(
    todo_id: str,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db),
):
    # Validate title if provided
    if todo.title is not None and not todo.title.strip():
        raise TodoTitleEmptyException(
            details="Title must not be empty or whitespace",
        )

    return crud.update_todo(db, todo_id, todo)

@router.patch(
    "/{todo_id}/toggle",
    response_model=schemas.TodoResponse,
    summary="Toggle todo completion",
)
def toggle_todo(todo_id: str, db: Session = Depends(get_db)):
    return crud.toggle_todo(db, todo_id)

@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
)
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)