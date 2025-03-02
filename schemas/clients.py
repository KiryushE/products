from pydantic import BaseModel
from typing import Optional


class ClientBase(BaseModel):
    name: str
    age: int


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


class ClientPublic(ClientBase):
    id: int