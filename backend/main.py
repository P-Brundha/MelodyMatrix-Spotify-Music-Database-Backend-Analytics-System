from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/artists")
def get_artists(db: Session = Depends(get_db)):
    return db.query(models.Artist).all()

@app.get("/tracks")
def get_tracks(db: Session = Depends(get_db)):
    return db.query(models.Track).all()
