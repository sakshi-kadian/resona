"""
Temporal Features Module

Extracts temporal patterns from listening history:
- Peak listening hours
- Weekend vs weekday patterns
- Listening time distribution
"""

from typing import Dict, List, Any
from datetime import datetime
from collections import Counter
import numpy as np

class TemporalFeatures:
    """Extract temporal features from listening data"""
    
    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize with user data
        
        Args:
            user_data: Complete user data from Spotify
        """
        self.user_data = user_data
        self.recently_played = user_data.get('recently_played', [])
    
    def calculate_peak_listening_hour(self) -> int:
        """
        Calculate the hour of day when user listens most
        
        Returns:
            int: Peak hour (0-23)
        """
        hours = []
        
        for item in self.recently_played:
            if item.get('played_at'):
                try:
                    # Parse ISO timestamp
                    played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
                    hours.append(played_at.hour)
                except:
                    continue
        
        if not hours:
            return 12  # Default to noon
        
        # Find most common hour
        hour_counts = Counter(hours)
        peak_hour = hour_counts.most_common(1)[0][0]
        
        return peak_hour
    
    def calculate_weekend_ratio(self) -> float:
        """
        Calculate ratio of weekend vs weekday listening
        
        Returns:
            float: Weekend ratio (0-1, higher = more weekend listening)
        """
        weekend_plays = 0
        weekday_plays = 0
        
        for item in self.recently_played:
            if item.get('played_at'):
                try:
                    played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
                    # 5 = Saturday, 6 = Sunday
                    if played_at.weekday() >= 5:
                        weekend_plays += 1
                    else:
                        weekday_plays += 1
                except:
                    continue
        
        total_plays = weekend_plays + weekday_plays
        if total_plays == 0:
            return 0.5  # Default middle value
        
        weekend_ratio = weekend_plays / total_plays
        
        return round(weekend_ratio, 3)
    
    def calculate_listening_time_variance(self) -> float:
        """
        Calculate variance in listening times (consistency)
        
        Returns:
            float: Time variance (0-1, higher = more varied listening times)
        """
        hours = []
        
        for item in self.recently_played:
            if item.get('played_at'):
                try:
                    played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
                    hours.append(played_at.hour)
                except:
                    continue
        
        if len(hours) < 2:
            return 0.5
        
        # Calculate standard deviation and normalize to 0-1
        std_dev = np.std(hours)
        # Max std dev for 24 hours is ~6.9, normalize to 0-1
        variance = min(std_dev / 7.0, 1.0)
        
        return round(variance, 3)
    
    def extract_all_features(self) -> Dict[str, Any]:
        """
        Extract all temporal features
        
        Returns:
            dict: All temporal features
        """
        return {
            "peak_listening_hour": self.calculate_peak_listening_hour(),
            "weekend_ratio": self.calculate_weekend_ratio(),
            "listening_time_variance": self.calculate_listening_time_variance()
        }
