import json
import os
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

MONGODB_URL = os.environ.get("MONGODB_URL", "")

app = FastAPI()

# MongoDB configuration

client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_database("todo")
todo_collection = db.get_collection("todos")

PyObjectId = Annotated[str, BeforeValidator(str)]


class TodoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, return_in_api=False)
    name: str
    description: str | None = None
    creation_datetime: datetime | None = Field(default=datetime.now())
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Wash the dishes",
                "description": "Wash the dishes on Monday afternoon",
                "start_datetime": "2024-08-14T02:37:36.936Z",
                "end_datetime": "2024-08-14T02:37:36.936Z",
            }
        },
    )


class UpdateTodoModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

class TodoResponseModel(BaseModel):
    name: str
    description: Optional[str] = None
    creation_datetime: Optional[datetime] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None


class TodoCollection(BaseModel):
    todos: List[TodoResponseModel]


@app.post(
    "/todos/",
    response_description="Add new ToDo",
    response_model=TodoModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_todo(todo: TodoModel = Body(...)) -> TodoResponseModel:
    try:
        new_todo = await todo_collection.insert_one(
            todo.model_dump(by_alias=True, exclude=["id"])
        )
        created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
        return created_todo
    except Exception as e:
        print(f"Failed with error {e}")


@app.get("/todos/", response_model_by_alias=False)
async def read_todos():
    return TodoCollection(todos=await todo_collection.find().to_list(10))
