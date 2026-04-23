from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import date
import os

from ..database import get_db
from ..models import Track, Category, ArtistGroup, TrackDetail, NewRelease
from ..schemas import TrackCreate, TrackDetailCreate, CategoryCreate, ArtistCreate

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# ============ IP SECURITY CONFIGURATION ============
# Allowed IP addresses for admin access (from your ipconfig)
ALLOWED_ADMIN_IPS = [
    '127.0.0.1',           # Localhost
    '::1',                 # Localhost IPv6
    '10.63.192.8',         # Your Wi-Fi IP
    '172.20.16.1',         # Your WSL IP
    '172.16.1.10',         # VMware VMnet1
    '172.16.10.1',         # VMware VMnet2
    '172.16.20.1',         # VMware VMnet3
    '192.168.1.100',   
        '35.197.0.0/16',
    '34.120.0.0/16',
    '35.197.0.0/16',# Common local IP (add if needed)
]

# Allowed domains (add your domain when deployed)
ALLOWED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    '10.63.192.8',
    # Add your production domain when deployed:
    # 'yourdomain.com',
    # 'www.yourdomain.com',
     'chncam.netlify.app',        # ← ADD THIS
    'cheahun.netlify.app',       # ← ADD THIS
    'www.chncam.site',
]

def verify_admin_access(request: Request):
    """Verify that the request comes from an allowed IP or domain"""
    client_ip = request.client.host
    origin = request.headers.get("origin", "")
    referer = request.headers.get("referer", "")
    
    # Check if IP is allowed
    if client_ip in ALLOWED_ADMIN_IPS:
        return True
    
    # Check if origin/referer is from allowed domain
    for domain in ALLOWED_DOMAINS:
        if domain in origin or domain in referer:
            return True
    
    # Log unauthorized access attempt
    print(f"🚨 Unauthorized admin access attempt from IP: {client_ip}, Origin: {origin}")
    raise HTTPException(status_code=403, detail="Access denied. Admin access restricted to authorized IPs only.")
    
    return True

# ============ TRACKS ============
@router.post("/tracks")
def create_track(
    track: TrackCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    new_track = Track(**track.dict())
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return {"success": True, "id": new_track.id, "message": "Track created"}

@router.put("/tracks/{track_id}")
def update_track(
    track_id: int, 
    track: TrackCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_track = db.query(Track).filter(Track.id == track_id).first()
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    for key, value in track.dict().items():
        setattr(db_track, key, value)
    
    db.commit()
    return {"success": True, "message": "Track updated"}

@router.delete("/tracks/{track_id}")
def delete_track(
    track_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_track = db.query(Track).filter(Track.id == track_id).first()
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    db.delete(db_track)
    db.commit()
    return {"success": True, "message": "Track deleted"}

# ============ TRACK DETAILS ============
@router.post("/tracks/{track_id}/detail")
def add_track_detail(
    track_id: int, 
    detail: TrackDetailCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    existing = db.query(TrackDetail).filter(TrackDetail.track_id == track_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Detail already exists, use PUT to update")
    
    new_detail = TrackDetail(track_id=track_id, **detail.dict())
    db.add(new_detail)
    db.commit()
    return {"success": True, "message": "Track detail added"}

@router.put("/tracks/{track_id}/detail")
def update_track_detail(
    track_id: int, 
    detail: TrackDetailCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_detail = db.query(TrackDetail).filter(TrackDetail.track_id == track_id).first()
    if not db_detail:
        raise HTTPException(status_code=404, detail="Track detail not found")
    
    for key, value in detail.dict().items():
        setattr(db_detail, key, value)
    
    db.commit()
    return {"success": True, "message": "Track detail updated"}

# ============ CATEGORIES ============
@router.post("/categories")
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"success": True, "id": new_category.id, "message": "Category created"}

@router.put("/categories/{category_id}")
def update_category(
    category_id: int, 
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    return {"success": True, "message": "Category updated"}

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return {"success": True, "message": "Category deleted"}

# ============ ARTISTS ============
@router.post("/artists")
def create_artist(
    artist: ArtistCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    new_artist = ArtistGroup(**artist.dict())
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return {"success": True, "id": new_artist.id, "message": "Artist created"}

@router.put("/artists/{artist_id}")
def update_artist(
    artist_id: int, 
    artist: ArtistCreate, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_artist = db.query(ArtistGroup).filter(ArtistGroup.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    for key, value in artist.dict().items():
        setattr(db_artist, key, value)
    
    db.commit()
    return {"success": True, "message": "Artist updated"}

@router.delete("/artists/{artist_id}")
def delete_artist(
    artist_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_artist = db.query(ArtistGroup).filter(ArtistGroup.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    db.delete(db_artist)
    db.commit()
    return {"success": True, "message": "Artist deleted"}

# ============ NEW RELEASES ============

@router.get("/new-releases")
def get_new_releases(db: Session = Depends(get_db)):
    """Get all new releases with track details (public endpoint)"""
    results = db.query(
        NewRelease.id,
        NewRelease.track_id,  # ← THIS IS WHAT YOU NEED
        NewRelease.release_status,
        NewRelease.release_date,
        NewRelease.is_featured,
        Track.id.label("track_id"),
        Track.title,
        Track.cover_image,
        Track.duration,
        Track.release_date.label("track_release_date"),
        ArtistGroup.name.label("artist_name"),
        Category.name.label("category")
    ).join(
        Track, NewRelease.track_id == Track.id
    ).outerjoin(
        ArtistGroup, Track.artist_group_id == ArtistGroup.id
    ).outerjoin(
        Category, Track.category_id == Category.id
    ).filter(
        Track.is_published == True
    ).order_by(
        NewRelease.release_date.desc()
    ).all()
    
    # Convert to list of dicts
    return [
        {
            "id": r.id,
            "track_id": r.track_id,  # ← THIS WILL NOW EXIST
            "release_status": r.release_status,
            "release_date": r.release_date,
            "is_featured": r.is_featured,
            "title": r.title,
            "cover_image": r.cover_image,
            "duration": r.duration,
            "artist_name": r.artist_name,
            "category": r.category
        }
        for r in results
    ]


@router.post("/new-releases")
def add_new_release(
    track_id: int, 
    release_status: str = "upcoming", 
    is_featured: bool = False,
    release_date: str = None,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    # Check if already exists
    existing = db.query(NewRelease).filter(NewRelease.track_id == track_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Track already in new releases")
    
    # Get track
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    # Use provided release_date or track's release_date
    if release_date:
        final_release_date = release_date
    elif track.release_date:
        final_release_date = track.release_date
    else:
        final_release_date = date.today().isoformat()
    
    print(f"Creating new release with release_date: {final_release_date}")
    
    new_release = NewRelease(
        track_id=track_id,
        release_status=release_status,
        release_date=final_release_date,
        is_featured=is_featured
    )
    db.add(new_release)
    db.commit()
    db.refresh(new_release)
    return {"success": True, "id": new_release.id, "message": "Added to new releases"}

@router.put("/new-releases/{track_id}")
def update_release_status(
    track_id: int, 
    release_status: str, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_release = db.query(NewRelease).filter(NewRelease.track_id == track_id).first()
    if not db_release:
        raise HTTPException(status_code=404, detail="Release not found")
    
    db_release.release_status = release_status
    db.commit()
    return {"success": True, "message": "Release status updated"}

@router.delete("/new-releases/{track_id}")
def remove_new_release(
    track_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    db_release = db.query(NewRelease).filter(NewRelease.track_id == track_id).first()
    if not db_release:
        raise HTTPException(status_code=404, detail="Release not found")
    
    db.delete(db_release)
    db.commit()
    return {"success": True, "message": "Removed from new releases"}


