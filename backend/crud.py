from sqlalchemy.orm import Session
import models, schemas
from passlib.hash import bcrypt

# ---------- User ----------
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = bcrypt.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---------- Blog ----------
def create_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    db_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        author_id=user_id
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def get_blogs_by_user(db: Session, user_id: int):
    return db.query(models.Blog).filter(models.Blog.author_id == user_id).all()

def update_blog(db: Session, blog_id: int, blog: schemas.BlogCreate, user_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog and db_blog.author_id == user_id:
        db_blog.title = blog.title
        db_blog.content = blog.content
        db_blog.image_url = blog.image_url
        db.commit()
        db.refresh(db_blog)
        return db_blog
    return None

def delete_blog(db: Session, blog_id: int, user_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog and db_blog.author_id == user_id:
        db.delete(db_blog)
        db.commit()
        return True
    return False

# ---------- Comment ----------
def add_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(
        content=comment.content,
        blog_id=comment.blog_id,
        author_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int, user_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment and db_comment.author_id == user_id:
        db.delete(db_comment)
        db.commit()
        return True
    return False