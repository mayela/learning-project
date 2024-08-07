import pickle
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    name: str
    description: str | None = None
    creation_datetime : datetime | None = None
    start_datetime : datetime | None = None
    end_datetime : datetime | None = None

@app.post("/todos/")
async def create_todo(todo: Todo) -> Todo:
    with open('todos', 'w+b') as f:
        try:
            todo_data = pickle.load(file) 
            todo_data.append(str(todo))
            pickle.dump(todo_data, todos)
            return todo
        except Exception as e:
            print(f"Failed with error {e}")

@app.get("/todos/")
async def read_todos() -> list[Todo]:
    file = open('todos', 'rb')
    todo_data = pickle.load(file)
    file.close()
    return [
        Todo(name="Wash dishes"),
        Todo(name="Make lunch"),
    ]
