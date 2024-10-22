from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# from models import models
from . import models
from .database import SessionLocal, engine
from . import schemas
import language_tool_python


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/check-grammar", response_model=schemas.GrammarResponse)
async def check_grammar(note: schemas.NoteCreate) -> schemas.GrammarResponse:
    return chechGrammar(note)


def chechGrammar(note: schemas.NoteCreate):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(note.content)

    # tool.close()
    print(matches)
    if len(matches) > 0:
        number = len(matches)
        mistakes = []
        for mistake in matches:
            # print('message:', mistake.message)
            # print('replacements:', mistake.replacements)
            # print('offset:', mistake.offset)
            # # print('length:', mistake.length)
            mistakes.append(schemas.Mistake(message=mistake.message, offset=mistake.offset, suggestionsToFix=mistake.replacements))
        return schemas.GrammarResponse(suggestion=tool.correct(note.content), numberOfMistakes=number, mistakes=mistakes)
    else:
        return schemas.GrammarResponse(suggestion="No grammar mistakes found", numberOfMistakes=0, mistakes=None)