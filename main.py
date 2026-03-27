from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Note
import json
import redis.asyncio as redis
import os 



redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    decode_responses=True
)


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Rajendra Channel")

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    cached_notes = await redis_client.get("notes")
    if cached_notes:
        notes = json.loads(cached_notes)
    else:
        notes = db.query(Note).all()
        
        # convert SQLAlchemy objects to dict
        notes = [{"id": n.id, "content": n.content} for n in notes]

        await redis_client.set("notes", json.dumps(notes), ex=60)  # cache 60 sec

    return templates.TemplateResponse(
        request=request,
        name="index.html",   # MUST be string
        context = {
            "channel_name": "DevOps Rajendra",
            "description": "Learn Docker, Kubernetes, AWS, DevOps & Python in Telugu.",
            "author": "Rajendra Taidala",
            "notes": notes
        }
    )

@app.post("/add", response_class=HTMLResponse)
async def add_note(
    request: Request,
    note: str = Form(...),
    db: Session = Depends(get_db)
):
    new_note = Note(content=note)
    db.add(new_note)
    db.commit()

    # ❗ invalidate cache
    await redis_client.delete("notes")
    
    notes = db.query(Note).all()
    #notes = [{"id": n.id, "content": n.content} for n in notes_db]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context = {
            "request": request,
            "channel_name": "DevOps Rajendra",
            "description": "Learn Docker, Kubernetes, AWS, DevOps & Python in Telugu.",
            "author": "Rajendra Taidala",
            "notes": notes
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "OK"}
