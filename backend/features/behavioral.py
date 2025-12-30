"""
Behavioral Features Module

Extracts behavioral patterns from user's listening history:
- Repeat rate (how often tracks are repeated)
- Exploration score (diversity of listening)
- Track loyalty (sticking to favorites vs discovering new)
- Artist diversity
- Listening consistency
"""

from typing import Dict, List, Any
from collections import Counter
import numpy as np

class BehavioralFeatures:
    """Extract behavioral features from listening data"""
    
    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize with user data
        
        Args:
            user_data: Complete user data from Spotify
        """
        self.user_data = user_data
        self.top_tracks_short = user_data.get('top_tracks_short', [])
        self.top_tracks_medium = user_data.get('top_tracks_medium', [])
        self.top_tracks_long = user_data.get('top_tracks_long', [])
        self.recently_played = user_data.get('recently_played', [])
    
    def calculate_repeat_rate(self) -> float:
        """
        Calculate how often user repeats tracks
        
        Returns:
            float: Repeat rate (0-1, higher = more repetition)
        """
        # Get all recently played track IDs
        recent_track_ids = [item['track']['id'] for item in self.recently_played 
                           if item.get('track') and item['track'].get('id')]
        
        if not recent_track_ids:
            return 0.0
        
        # Count unique vs total
        unique_tracks = len(set(recent_track_ids))
        total_tracks = len(recent_track_ids)
        
        # Repeat rate = 1 - (unique/total)
        repeat_rate = 1 - (unique_tracks / total_tracks)
        
        return round(repeat_rate, 3)
    
    def calculate_exploration_score(self) -> float:
        """
        Calculate how much user explores new music
        
        Returns:
            float: Exploration score (0-1, higher = more exploration)
        """
        # Compare short-term vs long-term top tracks
        short_ids = set([t['id'] for t in self.top_tracks_short if t.get('id')])
        long_ids = set([t['id'] for t in self.top_tracks_long if t.get('id')])
        
        if not short_ids or not long_ids:
            return 0.5  # Default middle value
        
        # How many short-term tracks are NOT in long-term?
        new_tracks = short_ids - long_ids
        exploration_score = len(new_tracks) / len(short_ids)
        
        return round(exploration_score, 3)
    
    def calculate_artist_diversity(self) -> float:
        """
        Calculate diversity of artists in listening history
        
        Returns:
            float: Artist diversity score (0-1, higher = more diverse)
        """
        # Get all artists from top tracks
        all_artists = []
        for track in self.top_tracks_medium:
            if track.get('artists'):
                all_artists.extend([artist['id'] for artist in track['artists']])
        
        if not all_artists:
            return 0.0
        
        # Calculate diversity using unique ratio
        unique_artists = len(set(all_artists))
        total_artist_mentions = len(all_artists)
        
        diversity = unique_artists / total_artist_mentions
        
        return round(diversity, 3)
    
    def calculate_track_loyalty(self) -> float:
        """
        Calculate how loyal user is to favorite tracks
        
        Returns:
            float: Loyalty score (0-1, higher = more loyal to favorites)
        """
        # Get top 10 tracks from medium term
        top_10_ids = set([t['id'] for t in self.top_tracks_medium[:10] if t.get('id')])
        
        # How many of recently played are in top 10?
        recent_ids = [item['track']['id'] for item in self.recently_played 
                     if item.get('track') and item['track'].get('id')]
        
        if not recent_ids:
            return 0.0
        
        top_10_plays = sum(1 for track_id in recent_ids if track_id in top_10_ids)
        loyalty = top_10_plays / len(recent_ids)
        
        return round(loyalty, 3)
    
    def calculate_listening_consistency(self) -> float:
        """
        Calculate consistency of listening patterns
        
        Returns:
            float: Consistency score (0-1, higher = more consistent)
        """
        # Compare overlap between short, medium, and long term
        short_ids = set([t['id'] for t in self.top_tracks_short if t.get('id')])
        medium_ids = set([t['id'] for t in self.top_tracks_medium if t.get('id')])
        long_ids = set([t['id'] for t in self.top_tracks_long if t.get('id')])
        
        if not short_ids or not medium_ids or not long_ids:
            return 0.5
        
        # Calculate overlap
        short_medium_overlap = len(short_ids & medium_ids) / len(short_ids)
        medium_long_overlap = len(medium_ids & long_ids) / len(medium_ids)
        
        consistency = (short_medium_overlap + medium_long_overlap) / 2
        
        return round(consistency, 3)
    
    def extract_all_features(self) -> Dict[str, float]:
        """
        Extract all behavioral features
        
        Returns:
            dict: All behavioral features
        """
        return {
            "repeat_rate": self.calculate_repeat_rate(),
            "exploration_score": self.calculate_exploration_score(),
            "artist_diversity": self.calculate_artist_diversity(),
            "track_loyalty": self.calculate_track_loyalty(),
            "listening_consistency": self.calculate_listening_consistency()
        }
