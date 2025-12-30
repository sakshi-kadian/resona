"""
Database Storage Service

Replaces JSON file storage with SQLite database
"""

from sqlalchemy.orm import Session
from database.models import UserData, UserFeatures
from database.db import get_db
from datetime import datetime
from typing import Dict, Any, Optional
import json

class DatabaseStorage:
    """Manages storage using SQLite database"""
    
    def save_user_data(self, user_id: str, data: Dict[str, Any], db: Session) -> None:
        """
        Save user's Spotify data to database
        
        Args:
            user_id: Spotify user ID
            data: User data from Spotify
            db: Database session
        """
        # Check if user exists
        user_data = db.query(UserData).filter(UserData.user_id == user_id).first()
        
        if user_data:
            # Update existing
            user_data.profile = json.dumps(data.get('profile', {}))
            user_data.top_tracks_short = json.dumps(data.get('top_tracks_short', []))
            user_data.top_tracks_medium = json.dumps(data.get('top_tracks_medium', []))
            user_data.top_tracks_long = json.dumps(data.get('top_tracks_long', []))
            user_data.recently_played = json.dumps(data.get('recently_played', []))
            user_data.artists = json.dumps(data.get('artists', []))
            user_data.fetched_at = datetime.fromisoformat(data.get('fetched_at', datetime.utcnow().isoformat()))
            user_data.saved_at = datetime.utcnow()
        else:
            # Create new
            user_data = UserData(
                user_id=user_id,
                profile=json.dumps(data.get('profile', {})),
                top_tracks_short=json.dumps(data.get('top_tracks_short', [])),
                top_tracks_medium=json.dumps(data.get('top_tracks_medium', [])),
                top_tracks_long=json.dumps(data.get('top_tracks_long', [])),
                recently_played=json.dumps(data.get('recently_played', [])),
                artists=json.dumps(data.get('artists', [])),
                fetched_at=datetime.fromisoformat(data.get('fetched_at', datetime.utcnow().isoformat())),
                saved_at=datetime.utcnow()
            )
            db.add(user_data)
        
        db.commit()
        print(f"💾 Saved user data to database for user: {user_id}")
    
    def load_user_data(self, user_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        Load user's Spotify data from database
        
        Args:
            user_id: Spotify user ID
            db: Database session
            
        Returns:
            dict: User data or None if not found
        """
        user_data = db.query(UserData).filter(UserData.user_id == user_id).first()
        
        if not user_data:
            return None
        
        print(f"📂 Loaded user data from database for user: {user_id}")
        return user_data.to_dict()
    
    def save_features(self, user_id: str, features_data: Dict[str, Any], db: Session) -> None:
        """
        Save computed features to database
        
        Args:
            user_id: Spotify user ID
            features_data: Computed features
            db: Database session
        """
        features = features_data.get('features', {})
        summary = features_data.get('summary', {})
        
        # Check if features exist
        user_features = db.query(UserFeatures).filter(UserFeatures.user_id == user_id).first()
        
        if user_features:
            # Update existing
            self._update_features(user_features, features, summary)
        else:
            # Create new
            user_features = UserFeatures(user_id=user_id)
            self._update_features(user_features, features, summary)
            db.add(user_features)
        
        db.commit()
        print(f"💾 Saved features to database for user: {user_id}")
    
    def _update_features(self, user_features: UserFeatures, features: Dict, summary: Dict):
        """Helper to update feature fields"""
        # Behavioral
        behavioral = features.get('behavioral', {})
        user_features.repeat_rate = behavioral.get('repeat_rate')
        user_features.exploration_score = behavioral.get('exploration_score')
        user_features.artist_diversity = behavioral.get('artist_diversity')
        user_features.track_loyalty = behavioral.get('track_loyalty')
        user_features.listening_consistency = behavioral.get('listening_consistency')
        
        # Temporal
        temporal = features.get('temporal', {})
        user_features.peak_listening_hour = temporal.get('peak_listening_hour')
        user_features.weekend_ratio = temporal.get('weekend_ratio')
        user_features.listening_time_variance = temporal.get('listening_time_variance')
        
        # Track metadata
        metadata = features.get('track_metadata', {})
        user_features.avg_popularity = metadata.get('avg_popularity')
        user_features.avg_duration_minutes = metadata.get('avg_duration_minutes')
        user_features.track_age_preference = metadata.get('track_age_preference')
        
        # Genre
        genre = features.get('genre', {})
        user_features.genre_diversity = genre.get('genre_diversity')
        user_features.genre_uniqueness = genre.get('genre_uniqueness')
        user_features.total_unique_genres = genre.get('total_unique_genres')
        user_features.top_genres = json.dumps(genre.get('top_genres', []))
        user_features.genre_distribution = json.dumps(genre.get('genre_distribution', {}))
        
        # Summary
        user_features.listening_style = summary.get('listening_style')
        user_features.peak_time = summary.get('peak_time')
        user_features.music_taste = summary.get('music_taste')
        user_features.diversity_level = summary.get('diversity_level')
        user_features.computed_at = datetime.utcnow()
    
    def load_features(self, user_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        Load computed features from database
        
        Args:
            user_id: Spotify user ID
            db: Database session
            
        Returns:
            dict: Features or None if not found
        """
        user_features = db.query(UserFeatures).filter(UserFeatures.user_id == user_id).first()
        
        if not user_features:
            return None
        
        print(f"📂 Loaded features from database for user: {user_id}")
        return user_features.to_dict()
    
    def data_exists(self, user_id: str, db: Session) -> bool:
        """Check if user data exists"""
        return db.query(UserData).filter(UserData.user_id == user_id).first() is not None
    
    def features_exist(self, user_id: str, db: Session) -> bool:
        """Check if features exist"""
        return db.query(UserFeatures).filter(UserFeatures.user_id == user_id).first() is not None
    
    def get_data_age(self, user_id: str, db: Session) -> Optional[float]:
        """
        Get age of cached data in hours
        
        Args:
            user_id: Spotify user ID
            db: Database session
            
        Returns:
            float: Age in hours or None if no data
        """
        user_data = db.query(UserData).filter(UserData.user_id == user_id).first()
        
        if not user_data or not user_data.saved_at:
            return None
        
        age = (datetime.utcnow() - user_data.saved_at).total_seconds() / 3600
        return age

# Global storage instance
db_storage = DatabaseStorage()
