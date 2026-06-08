import os
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import User, Post, SiteSetting, Message, Photo, Diary, Tool
from schemas import (
    PostCreate, PostUpdate, PostOut, PostListItem,
    LoginRequest, TokenResponse, UserUpdate, UserOut,
    MessageCreate, MessageOut,
    PhotoCreate, PhotoUpdate, PhotoOut,
    DiaryCreate, DiaryUpdate, DiaryOut,
    ToolCreate, ToolUpdate, ToolOut,
)
from auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.on_event("startup")
def init_admin_and_settings():
    from database import SessionLocal
    db = SessionLocal()
    if not db.query(User).filter(User.username == "admin").first():
        db.add(User(username="admin", hashed_password=hash_password("admin123"), nickname="博主"))
        db.commit()
    for key in ["background_image"]:
        if not db.query(SiteSetting).filter(SiteSetting.key == key).first():
            db.add(SiteSetting(key=key, value=""))
            db.commit()
    db.close()


# ---- Auth ----

@app.post("/api/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return TokenResponse(access_token=create_access_token({"sub": user.username}))

@app.get("/api/user", response_model=UserOut)
def get_user(user: User = Depends(get_current_user)):
    return user

@app.put("/api/user", response_model=UserOut)
def update_user(data: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.nickname is not None:
        user.nickname = data.nickname
    db.commit()
    db.refresh(user)
    return user

@app.post("/api/user/avatar", response_model=UserOut)
def upload_avatar(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ext = file.filename.split(".")[-1] if "." in file.filename else "png"
    filename = f"avatar_{user.id}_{int(datetime.now().timestamp())}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    content = file.file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    user.avatar = f"/uploads/{filename}"
    db.commit()
    db.refresh(user)
    return user


# ---- Posts ----

@app.get("/api/posts", response_model=list[PostListItem])
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).all()

@app.get("/api/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    return post

@app.post("/api/posts", response_model=PostOut)
def create_post(data: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = Post(title=data.title, content=data.content, summary=data.summary)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.put("/api/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, data: PostUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    if data.title is not None:
        post.title = data.title
    if data.content is not None:
        post.content = data.content
    if data.summary is not None:
        post.summary = data.summary
    post.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(post)
    db.commit()
    return {"ok": True}


# ---- Media Upload ----

@app.post("/api/upload")
def upload_media(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    filename = f"{int(datetime.now().timestamp())}_{user.id}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    content = file.file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    return {"url": f"/uploads/{filename}"}


# ---- Site Settings ----

@app.get("/api/settings")
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSetting).all()
    result = {s.key: s.value for s in settings}
    return result

@app.put("/api/settings")
def update_settings(
    data: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for key, value in data.items():
        setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
        if setting:
            setting.value = value
    db.commit()
    settings = db.query(SiteSetting).all()
    return {s.key: s.value for s in settings}


# ---- Messages / Guestbook ----

@app.get("/api/messages", response_model=list[MessageOut])
def list_messages(db: Session = Depends(get_db)):
    return db.query(Message).order_by(Message.created_at.desc()).all()

@app.post("/api/messages", response_model=MessageOut)
def create_message(data: MessageCreate, db: Session = Depends(get_db)):
    msg = Message(name=data.name, content=data.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


# ---- Photos / Album ----

@app.get("/api/photos", response_model=list[PhotoOut])
def list_photos(db: Session = Depends(get_db)):
    return db.query(Photo).order_by(Photo.created_at.desc()).all()

@app.post("/api/photos", response_model=PhotoOut)
def create_photo(
    file: UploadFile = File(...),
    title: str = Form(""),
    description: str = Form(""),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"photo_{int(datetime.now().timestamp())}_{user.id}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    content = file.file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    photo = Photo(title=title, description=description, url=f"/uploads/{filename}")
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

@app.put("/api/photos/{photo_id}", response_model=PhotoOut)
def update_photo(photo_id: int, data: PhotoUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在")
    if data.title is not None:
        photo.title = data.title
    if data.description is not None:
        photo.description = data.description
    db.commit()
    db.refresh(photo)
    return photo

@app.delete("/api/photos/{photo_id}")
def delete_photo(photo_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在")
    db.delete(photo)
    db.commit()
    return {"ok": True}


# ---- Diaries ----

@app.get("/api/diaries", response_model=list[DiaryOut])
def list_diaries(db: Session = Depends(get_db)):
    return db.query(Diary).order_by(Diary.created_at.desc()).all()

@app.post("/api/diaries", response_model=DiaryOut)
def create_diary(data: DiaryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    diary = Diary(title=data.title, content=data.content, mood=data.mood)
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary

@app.put("/api/diaries/{diary_id}", response_model=DiaryOut)
def update_diary(diary_id: int, data: DiaryUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")
    if data.title is not None:
        diary.title = data.title
    if data.content is not None:
        diary.content = data.content
    if data.mood is not None:
        diary.mood = data.mood
    db.commit()
    db.refresh(diary)
    return diary

@app.delete("/api/diaries/{diary_id}")
def delete_diary(diary_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在")
    db.delete(diary)
    db.commit()
    return {"ok": True}


# ---- Tools ----

@app.get("/api/tools", response_model=list[ToolOut])
def list_tools(db: Session = Depends(get_db)):
    return db.query(Tool).order_by(Tool.created_at.desc()).all()

@app.post("/api/tools", response_model=ToolOut)
def create_tool(data: ToolCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tool = Tool(name=data.name, description=data.description, url=data.url, category=data.category)
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool

@app.put("/api/tools/{tool_id}", response_model=ToolOut)
def update_tool(tool_id: int, data: ToolUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    if data.name is not None:
        tool.name = data.name
    if data.description is not None:
        tool.description = data.description
    if data.url is not None:
        tool.url = data.url
    if data.category is not None:
        tool.category = data.category
    db.commit()
    db.refresh(tool)
    return tool

@app.delete("/api/tools/{tool_id}")
def delete_tool(tool_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    db.delete(tool)
    db.commit()
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
