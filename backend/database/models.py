"""
Database Models

SQLAlchemy models for storing user data and features
"""

from sqlalchemy import Column, String, Text, DateTime, Float, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()

class UserData(Base):
    """Store user's Spotify data"""
    __tablename__ = 'user_data'
    
    user_id = Column(String(100), primary_key=True)
    profile = Column(Text)  # JSON string
    top_tracks_short = Column(Text)  # JSON string
    top_tracks_medium = Column(Text)  # JSON string
    top_tracks_long = Column(Text)  # JSON string
    recently_played = Column(Text)  # JSON string
    artists = Column(Text)  # JSON string
    fetched_at = Column(DateTime, default=datetime.utcnow)
    saved_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'profile': json.loads(self.profile) if self.profile else {},
            'top_tracks_short': json.loads(self.top_tracks_short) if self.top_tracks_short else [],
            'top_tracks_medium': json.loads(self.top_tracks_medium) if self.top_tracks_medium else [],
            'top_tracks_long': json.loads(self.top_tracks_long) if self.top_tracks_long else [],
            'recently_played': json.loads(self.recently_played) if self.recently_played else [],
            'artists': json.loads(self.artists) if self.artists else [],
            'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None,
            'saved_at': self.saved_at.isoformat() if self.saved_at else None,
            'from_cache': True,
            'cache_age_hours': (datetime.utcnow() - self.saved_at).total_seconds() / 3600 if self.saved_at else 0
        }

class UserFeatures(Base):
    """Store computed ML features"""
    __tablename__ = 'user_features'
    
    user_id = Column(String(100), primary_key=True)
    version = Column(String(10), default='1.0')
    
    # Behavioral features
    repeat_rate = Column(Float)
    exploration_score = Column(Float)
    artist_diversity = Column(Float)
    track_loyalty = Column(Float)
    listening_consistency = Column(Float)
    
    # Temporal features
    peak_listening_hour = Column(Integer)
    weekend_ratio = Column(Float)
    listening_time_variance = Column(Float)
    
    # Track metadata features
    avg_popularity = Column(Float)
    avg_duration_minutes = Column(Float)
    track_age_preference = Column(String(20))
    
    # Genre features
    genre_diversity = Column(Float)
    genre_uniqueness = Column(Float)
    total_unique_genres = Column(Integer)
    top_genres = Column(Text)  # JSON string
    genre_distribution = Column(Text)  # JSON string
    
    # Summary
    listening_style = Column(String(100))
    peak_time = Column(String(50))
    music_taste = Column(String(100))
    diversity_level = Column(String(50))
    
    computed_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'version': self.version,
            'features': {
                'behavioral': {
                    'repeat_rate': self.repeat_rate,
                    'exploration_score': self.exploration_score,
                    'artist_diversity': self.artist_diversity,
                    'track_loyalty': self.track_loyalty,
                    'listening_consistency': self.listening_consistency
                },
                'temporal': {
                    'peak_listening_hour': self.peak_listening_hour,
                    'weekend_ratio': self.weekend_ratio,
                    'listening_time_variance': self.listening_time_variance
                },
                'track_metadata': {
                    'avg_popularity': self.avg_popularity,
                    'avg_duration_minutes': self.avg_duration_minutes,
                    'track_age_preference': self.track_age_preference
                },
                'genre': {
                    'genre_diversity': self.genre_diversity,
                    'genre_uniqueness': self.genre_uniqueness,
                    'total_unique_genres': self.total_unique_genres,
                    'top_genres': json.loads(self.top_genres) if self.top_genres else [],
                    'genre_distribution': json.loads(self.genre_distribution) if self.genre_distribution else {}
                }
            },
            'summary': {
                'listening_style': self.listening_style,
                'peak_time': self.peak_time,
                'music_taste': self.music_taste,
                'diversity_level': self.diversity_level,
                'top_genres': json.loads(self.top_genres) if self.top_genres else []
            },
            'computed_at': self.computed_at.isoformat() if self.computed_at else None,
            'from_cache': True
        }
