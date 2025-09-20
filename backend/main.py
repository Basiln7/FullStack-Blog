from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os

from backend.database import Base, engine, SessionLocal
from backend import models, schemas, crud
from backend.auth import create_access_token, verify_password, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Auth ----------
@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ---------- Blogs ----------
@app.post("/blogs/", response_model=schemas.BlogOut)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_blog(db, blog, current_user.id)

@app.get("/blogs/", response_model=List[schemas.BlogOut])
def get_all_blogs(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_blogs_by_user(db, current_user.id)

@app.get("/blogs/{blog_id}", response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.put("/blogs/{blog_id}", response_model=schemas.BlogOut)
def update_blog(blog_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated = crud.update_blog(db, blog_id, blog, current_user.id)
    if not updated:
        raise HTTPException(status_code=403, detail="Not authorized or blog not found")
    return updated

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_blog(db, blog_id, current_user.id)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized or blog not found")
    return {"message": "Blog deleted"}

# ---------- Comments ----------
@app.post("/comments/", response_model=schemas.CommentOut)
def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.add_comment(db, comment, current_user.id)

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_comment(db, comment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized or comment not found")
    return {"message": "Comment deleted"}

# ---------- Static Frontend ----------
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
