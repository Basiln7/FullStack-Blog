import re
import uuid
import os
from fastapi import UploadFile
from typing import Optional

# ---------- Slug Generator ----------
def slugify(title: str) -> str:
    """
    Converts a blog title into a URL-friendly slug.
    Example: "My First Blog!" → "my-first-blog"
    """
    slug = re.sub(r"[^\w\s-]", "", title).strip().lower()
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug

# ---------- Unique Filename ----------
def generate_unique_filename(filename: str) -> str:
    """
    Adds a UUID to the filename to avoid collisions.
    Example: "image.png" → "image-abc123.png"
    """
    ext = filename.split(".")[-1]
    base = filename.rsplit(".", 1)[0]
    return f"{base}-{uuid.uuid4().hex[:8]}.{ext}"

# ---------- Save Uploaded Image ----------
def save_image(file: UploadFile, upload_dir: str = "uploads") -> Optional[str]:
    """
    Saves an uploaded image to disk and returns its path.
    """
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    filename = generate_unique_filename(file.filename)
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return filepath