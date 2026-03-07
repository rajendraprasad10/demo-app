from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Note

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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    notes = db.query(Note).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "channel_name": "DevOps Rajendra",
            "description": "Learn Docker, Kubernetes, AWS, DevOps & Python in Telugu.",
            "author": "Rajendra Taidala",
            "notes": notes
        },
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

    notes = db.query(Note).all()

    return templates.TemplateResponse(
        "index.html",
        {
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
