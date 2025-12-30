"""
Track Metadata Features Module

Extracts features from track metadata:
- Average popularity
- Duration patterns
- Track age preferences
"""

from typing import Dict, List, Any
import numpy as np
from datetime import datetime

class TrackMetadataFeatures:
    """Extract features from track metadata"""
    
    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize with user data
        
        Args:
            user_data: Complete user data from Spotify
        """
        self.user_data = user_data
        self.top_tracks_medium = user_data.get('top_tracks_medium', [])
    
    def calculate_avg_popularity(self) -> float:
        """
        Calculate average popularity of user's top tracks
        
        Returns:
            float: Average popularity (0-100)
        """
        popularities = [track.get('popularity', 0) for track in self.top_tracks_medium]
        
        if not popularities:
            return 50.0  # Default middle value
        
        avg_popularity = np.mean(popularities)
        
        return round(avg_popularity, 2)
    
    def calculate_avg_duration(self) -> float:
        """
        Calculate average track duration in minutes
        
        Returns:
            float: Average duration in minutes
        """
        durations_ms = [track.get('duration_ms', 0) for track in self.top_tracks_medium]
        
        if not durations_ms:
            return 3.5  # Default ~3.5 minutes
        
        avg_duration_minutes = np.mean(durations_ms) / 60000  # Convert ms to minutes
        
        return round(avg_duration_minutes, 2)
    
    def calculate_track_age_preference(self) -> str:
        """
        Calculate preference for new vs old tracks
        
        Returns:
            str: "new", "mixed", or "classic"
        """
        release_years = []
        
        for track in self.top_tracks_medium:
            if track.get('album') and track['album'].get('release_date'):
                try:
                    release_date = track['album']['release_date']
                    # Handle different date formats (YYYY, YYYY-MM, YYYY-MM-DD)
                    year = int(release_date.split('-')[0])
                    release_years.append(year)
                except:
                    continue
        
        if not release_years:
            return "mixed"
        
        current_year = datetime.now().year
        avg_year = np.mean(release_years)
        
        # Classify based on average year
        if avg_year >= current_year - 2:
            return "new"  # Mostly recent tracks
        elif avg_year >= current_year - 10:
            return "mixed"  # Mix of old and new
        else:
            return "classic"  # Prefers older tracks
    
    def extract_all_features(self) -> Dict[str, Any]:
        """
        Extract all track metadata features
        
        Returns:
            dict: All track metadata features
        """
        return {
            "avg_popularity": self.calculate_avg_popularity(),
            "avg_duration_minutes": self.calculate_avg_duration(),
            "track_age_preference": self.calculate_track_age_preference()
        }
