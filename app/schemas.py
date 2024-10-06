from pydantic import BaseModel
from uuid import UUID

class NoteBase(BaseModel):
    title: str
    content: str
    author_id: UUID

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class UserBase(BaseModel):
    username: str
    email: str

class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True