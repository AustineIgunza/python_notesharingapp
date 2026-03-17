"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============ User Schemas ============

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=4)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False
    admin_login: bool = False

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ Note Schemas ============

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_public: bool = False

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_public: Optional[bool] = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    author_id: int
    category_id: Optional[int]
    is_public: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============ Category Schemas ============

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ File Schemas ============

class NoteFileResponse(BaseModel):
    id: int
    note_id: int
    file_name: str
    file_size: int
    file_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# ============ Favorite Schemas ============

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    note_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ Authentication Schemas ============

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class VerifyOTP(BaseModel):
    email: EmailStr
    code: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    code: str
    new_password: str = Field(..., min_length=4)
    confirm_password: str = Field(..., min_length=4)

# ============ 2FA Schemas ============

class OTPResponse(BaseModel):
    success: bool
    message: str
    email: str

class SearchQuery(BaseModel):
    q: str = Field(..., min_length=3)
    category_id: Optional[int] = None
    page: int = Field(default=1, ge=1)
