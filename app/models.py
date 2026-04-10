from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, Index, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    tracks = relationship("Track", back_populates="category")

class ArtistGroup(Base):
    __tablename__ = "artist_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(Text)
    avatar_image = Column(Text)
    website_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    tracks = relationship("Track", back_populates="artist")

class Track(Base):
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    cover_image = Column(Text)
    duration = Column(String(20))
    release_date = Column(Date)
    is_published = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    artist_group_id = Column(Integer, ForeignKey("artist_groups.id", ondelete="SET NULL"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="tracks")
    artist = relationship("ArtistGroup", back_populates="tracks")
    detail = relationship("TrackDetail", back_populates="track", uselist=False)
    new_release = relationship("NewRelease", back_populates="track", uselist=False)

class TrackDetail(Base):
    __tablename__ = "tracks_detail"
    
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id", ondelete="CASCADE"), unique=True)
    youtube_link = Column(Text)
    full_description = Column(Text)
    lyrics = Column(Text)
    producer = Column(String(255))
    writer = Column(String(255))
    bpm = Column(Integer)
    key_signature = Column(String(10))
    total_plays = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    track = relationship("Track", back_populates="detail")

class NewRelease(Base):
    __tablename__ = "new_releases"
    
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id", ondelete="CASCADE"), unique=True)
    release_status = Column(String(50), default="upcoming")
    release_date = Column(Date, nullable=False)
    is_featured = Column(Boolean, default=False)
    days_countdown = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    track = relationship("Track", back_populates="new_release")

# Indexes
Index('idx_tracks_category', Track.category_id)
Index('idx_tracks_artist', Track.artist_group_id)
Index('idx_tracks_created', Track.created_at.desc())
Index('idx_tracks_published', Track.is_published)
Index('idx_new_releases_date', NewRelease.release_date.desc())
Index('idx_new_releases_status', NewRelease.release_status)