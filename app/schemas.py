from pydantic import BaseModel
from uuid import UUID
from typing import List
from language_tool_python import Match

class NoteBase(BaseModel):
    title: str | None = None
    content: str
    author_id: UUID | None = None

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

class Mistake(BaseModel):
    message: str
    offset: int
    suggestionsToFix: List[str]

class GrammarResponse(BaseModel):
    suggestion: str
    numberOfMistakes: int
    mistakes: List[Mistake] | None = None