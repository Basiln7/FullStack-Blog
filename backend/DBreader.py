from database import SessionLocal
import models

# Create a new DB session
db = SessionLocal()

# ---------- Read Users ----------
users = db.query(models.User).all()
print("Users:")
for user in users:
    print(f"ID: {user.id}, Username: {user.username}")

# ---------- Read Blogs ----------
blogs = db.query(models.Blog).all()
print("\nBlogs:")
for blog in blogs:
    print(f"ID: {blog.id}, Title: {blog.title}, Owner ID: {blog.owner_id}")

# ---------- Read Comments (if model exists) ----------
comments = db.query(models.Comment).all()
print("\nComments:")
for comment in comments:
    print(f"ID: {comment.id}, Content: {comment.content}, Blog ID: {comment.blog_id}, Author ID: {comment.owner_id}")

# Close the session
db.close()