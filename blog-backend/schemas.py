from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    summary: str = ""

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    summary: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class PostListItem(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    created_at: datetime
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    nickname: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: str
    model_config = {"from_attributes": True}

class SiteSettingOut(BaseModel):
    background_image: str = ""
    model_config = {"from_attributes": True}

class MessageCreate(BaseModel):
    name: str = "匿名"
    content: str

class MessageOut(BaseModel):
    id: int
    name: str
    content: str
    created_at: datetime
    model_config = {"from_attributes": True}

class PhotoCreate(BaseModel):
    title: str = ""
    description: str = ""

class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class PhotoOut(BaseModel):
    id: int
    title: str
    description: str
    url: str
    created_at: datetime
    model_config = {"from_attributes": True}

class DiaryCreate(BaseModel):
    title: str
    content: str
    mood: str = ""

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None

class DiaryOut(BaseModel):
    id: int
    title: str
    content: str
    mood: str
    created_at: datetime
    model_config = {"from_attributes": True}

class ToolCreate(BaseModel):
    name: str
    description: str = ""
    url: str
    category: str = "其他"

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None

class ToolOut(BaseModel):
    id: int
    name: str
    description: str
    url: str
    category: str
    created_at: datetime
    model_config = {"from_attributes": True}
