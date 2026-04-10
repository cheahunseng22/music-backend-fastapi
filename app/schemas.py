from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Artist Schemas
class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None
    avatar_image: Optional[str] = None
    website_url: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class ArtistResponse(ArtistBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Track Schemas (for card display)
class TrackResponse(BaseModel):
    id: int
    title: str
    cover_image: Optional[str] = None
    duration: Optional[str] = None
    category: Optional[str] = None
    artist_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# Track Detail Schema (for detail page)
class TrackDetailResponse(BaseModel):
    id: int
    title: str
    cover_image: Optional[str] = None
    duration: Optional[str] = None
    release_date: Optional[date] = None
    category: Optional[str] = None
    artist_name: Optional[str] = None
    artist_bio: Optional[str] = None
    youtube_link: Optional[str] = None
    full_description: Optional[str] = None
    lyrics: Optional[str] = None
    producer: Optional[str] = None
    writer: Optional[str] = None
    bpm: Optional[int] = None
    key_signature: Optional[str] = None
    total_plays: Optional[int] = None
    total_likes: Optional[int] = None
    release_status: Optional[str] = None
    is_featured: Optional[bool] = None
    
    class Config:
        from_attributes = True

# Track Create Schema
class TrackCreate(BaseModel):
    title: str
    cover_image: Optional[str] = None
    duration: Optional[str] = None
    release_date: Optional[date] = None
    category_id: Optional[int] = None
    artist_group_id: Optional[int] = None

# Track Detail Create Schema
class TrackDetailCreate(BaseModel):
    youtube_link: Optional[str] = None
    full_description: Optional[str] = None
    lyrics: Optional[str] = None
    producer: Optional[str] = None
    writer: Optional[str] = None
    bpm: Optional[int] = None
    key_signature: Optional[str] = None

# New Release Schema
class NewReleaseResponse(BaseModel):
    id: int
    title: str
    cover_image: Optional[str] = None
    artist_name: Optional[str] = None
    release_status: str
    release_date: date
    days_countdown: Optional[int] = None
    
    class Config:
        from_attributes = True