from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models import Track, Category, ArtistGroup, TrackDetail, NewRelease
from ..schemas import TrackResponse, TrackDetailResponse, CategoryResponse, ArtistResponse, NewReleaseResponse

router = APIRouter(prefix="/api", tags=["Public"])


@router.put("/tracks/{track_id}/play")
def increment_play_count(
    track_id: int,
    db: Session = Depends(get_db)
):
    """Public endpoint to increment track play count when clicked"""
    # Get the track detail (where total_plays actually lives)
    track_detail = db.query(TrackDetail).filter(TrackDetail.track_id == track_id).first()
    
    if not track_detail:
        # If no detail exists, create one
        track_detail = TrackDetail(track_id=track_id, total_plays=1)
        db.add(track_detail)
    else:
        # Increment play count by 1
        track_detail.total_plays = (track_detail.total_plays or 0) + 1
    
    db.commit()
    db.refresh(track_detail)
    
    return {
        "success": True,
        "track_id": track_id,
        "total_plays": track_detail.total_plays
    }


# 1. Get all tracks (for homepage cards)
@router.get("/tracks", response_model=list[TrackResponse])
def get_all_tracks(db: Session = Depends(get_db)):
    tracks = db.query(Track).filter(Track.is_published == True).all()

    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None,
            "total_plays": track.detail.total_plays if track.detail else 0
        })
    return result


@router.get("/tracks/search")
def search_tracks(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    tracks = db.query(Track).outerjoin(ArtistGroup).filter(
        or_(
            Track.title.ilike(f"%{q}%"),
            ArtistGroup.name.ilike(f"%{q}%")
        ),
        Track.is_published == True
    ).limit(20).all()
    
    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None
        })
    return result

# 9. Get featured tracks (MUST be before /tracks/{track_id})
@router.get("/tracks/featured")
def get_featured_tracks(db: Session = Depends(get_db)):
    tracks = db.query(Track).join(NewRelease).filter(
        NewRelease.is_featured == True,
        Track.is_published == True
    ).limit(10).all()
    
    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None
        })
    return result

# 2. Get single track with all details
@router.get("/tracks/{track_id}", response_model=TrackDetailResponse)
def get_track_detail(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id, Track.is_published == True).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    return {
        "id": track.id,
        "title": track.title,
        "cover_image": track.cover_image,
        "duration": track.duration,
        "release_date": track.release_date,
        "category": track.category.name if track.category else None,
        "artist_name": track.artist.name if track.artist else None,
        "artist_bio": track.artist.bio if track.artist else None,
        "youtube_link": track.detail.youtube_link if track.detail else None,
        "full_description": track.detail.full_description if track.detail else None,
        "lyrics": track.detail.lyrics if track.detail else None,
        "producer": track.detail.producer if track.detail else None,
        "writer": track.detail.writer if track.detail else None,
        "bpm": track.detail.bpm if track.detail else None,
        "key_signature": track.detail.key_signature if track.detail else None,
        "total_plays": track.detail.total_plays if track.detail else None,
        "total_likes": track.detail.total_likes if track.detail else None,
        "release_status": track.new_release.release_status if track.new_release else None,
        "is_featured": track.new_release.is_featured if track.new_release else None
    }

# 3. Get tracks by category
@router.get("/categories/{slug}/tracks", response_model=list[TrackResponse])
def get_tracks_by_category(slug: str, db: Session = Depends(get_db)):
    tracks = db.query(Track).join(Category).filter(
        Category.slug == slug,
        Track.is_published == True
    ).all()
    
    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None
        })
    return result

# 4. Get all categories
@router.get("/categories", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# 5. Get all artist groups
@router.get("/artists", response_model=list[ArtistResponse])
def get_all_artists(db: Session = Depends(get_db)):
    return db.query(ArtistGroup).all()

# 6. Get tracks by artist
@router.get("/artists/{artist_id}/tracks", response_model=list[TrackResponse])
def get_tracks_by_artist(artist_id: int, db: Session = Depends(get_db)):
    tracks = db.query(Track).filter(
        Track.artist_group_id == artist_id,
        Track.is_published == True
    ).all()
    
    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None
        })
    return result

# 7. Get new releases
@router.get("/new-releases", response_model=list[NewReleaseResponse])
def get_new_releases(db: Session = Depends(get_db)):
    releases = db.query(NewRelease).join(Track).filter(Track.is_published == True).all()
    
    result = []
    for release in releases:
        result.append({
            "id": release.id,
            "title": release.track.title,
            "cover_image": release.track.cover_image,
            "artist_name": release.track.artist.name if release.track.artist else None,
            "release_status": release.release_status,
            "release_date": release.release_date,
            "days_countdown": release.days_countdown
        })
    return result

# 8. Search tracks
@router.get("/tracks/search", response_model=list[TrackResponse])
def search_tracks(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    tracks = db.query(Track).outerjoin(ArtistGroup).filter(
        or_(
            Track.title.ilike(f"%{q}%"),
            ArtistGroup.name.ilike(f"%{q}%")
        ),
        Track.is_published == True
    ).limit(20).all()
    
    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None
        })
    return result

# 9. Get featured tracks
@router.get("/tracks/featured", response_model=list[TrackResponse])
def get_featured_tracks(db: Session = Depends(get_db)):
    tracks = db.query(Track).join(NewRelease).filter(
        NewRelease.is_featured == True,
        Track.is_published == True
    ).limit(10).all()
    
    result = []
    for track in tracks:
        result.append({
            "id": track.id,
            "title": track.title,
            "cover_image": track.cover_image,
            "duration": track.duration,
            "category": track.category.name if track.category else None,
            "artist_name": track.artist.name if track.artist else None
        })
    return result