from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ---------- User Schemas ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Comment Schemas ----------
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    blog_id: int

class CommentOut(CommentBase):
    id: int
    blog_id: int
    author_id: int
    class Config:
        from_attributes = True

# ---------- Blog Schemas ----------
class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None  # ✅ Added for image support

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    author_id: int
    comments: List[CommentOut] = []  # ✅ Nested comments for frontend rendering
    class Config:
        from_attributes = True

# ---------- Token Schemas ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None