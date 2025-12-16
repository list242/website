from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    director: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1888, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    description: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1888, le=2100)
    genre: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    description: Optional[str] = None

class Movie(MovieBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

