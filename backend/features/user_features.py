"""
User Features Module

Combines all feature extractors into a single user embedding vector
"""

from typing import Dict, Any
from features.behavioral import BehavioralFeatures
from features.temporal import TemporalFeatures
from features.track_metadata import TrackMetadataFeatures
from features.genre import GenreFeatures

class UserFeatures:
    """Combine all features into user embedding"""
    
    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize with user data
        
        Args:
            user_data: Complete user data from Spotify
        """
        self.user_data = user_data
        self.behavioral = BehavioralFeatures(user_data)
        self.temporal = TemporalFeatures(user_data)
        self.track_metadata = TrackMetadataFeatures(user_data)
        self.genre = GenreFeatures(user_data)
    
    def extract_all_features(self) -> Dict[str, Any]:
        """
        Extract all features from all modules
        
        Returns:
            dict: Complete feature set
        """
        print("🔧 Extracting features...")
        
        # Extract from each module
        behavioral_features = self.behavioral.extract_all_features()
        temporal_features = self.temporal.extract_all_features()
        metadata_features = self.track_metadata.extract_all_features()
        genre_features = self.genre.extract_all_features()
        
        print(f"✅ Behavioral features: {len(behavioral_features)}")
        print(f"✅ Temporal features: {len(temporal_features)}")
        print(f"✅ Metadata features: {len(metadata_features)}")
        print(f"✅ Genre features: {len(genre_features)}")
        
        # Combine all features
        all_features = {
            "behavioral": behavioral_features,
            "temporal": temporal_features,
            "track_metadata": metadata_features,
            "genre": genre_features
        }
        
        return all_features
    
    def get_feature_summary(self) -> Dict[str, Any]:
        """
        Get a human-readable summary of user's music profile
        
        Returns:
            dict: Feature summary
        """
        features = self.extract_all_features()
        
        # Create summary
        summary = {
            "listening_style": self._get_listening_style(features['behavioral']),
            "peak_time": self._get_peak_time_description(features['temporal']['peak_listening_hour']),
            "music_taste": self._get_music_taste_description(features),
            "top_genres": features['genre']['top_genres'][:5],
            "diversity_level": self._get_diversity_level(features['genre']['genre_diversity'])
        }
        
        return summary
    
    def _get_listening_style(self, behavioral: Dict[str, float]) -> str:
        """Describe listening style based on behavioral features"""
        if behavioral['exploration_score'] > 0.7:
            return "Explorer - Always discovering new music"
        elif behavioral['track_loyalty'] > 0.5:
            return "Loyalist - Sticks to favorites"
        elif behavioral['repeat_rate'] > 0.5:
            return "Repeater - Loves replaying tracks"
        else:
            return "Balanced - Mix of old and new"
    
    def _get_peak_time_description(self, hour: int) -> str:
        """Describe peak listening time"""
        if 6 <= hour < 12:
            return f"Morning listener ({hour}:00)"
        elif 12 <= hour < 17:
            return f"Afternoon listener ({hour}:00)"
        elif 17 <= hour < 22:
            return f"Evening listener ({hour}:00)"
        else:
            return f"Night owl ({hour}:00)"
    
    def _get_music_taste_description(self, features: Dict[str, Any]) -> str:
        """Describe music taste"""
        age_pref = features['track_metadata']['track_age_preference']
        popularity = features['track_metadata']['avg_popularity']
        
        if age_pref == "new" and popularity > 70:
            return "Trendsetter - Loves current hits"
        elif age_pref == "classic" and popularity < 50:
            return "Vintage connoisseur - Prefers classics"
        elif popularity > 70:
            return "Mainstream - Follows popular music"
        else:
            return "Indie explorer - Discovers hidden gems"
    
    def _get_diversity_level(self, diversity: float) -> str:
        """Describe genre diversity level"""
        if diversity > 0.8:
            return "Very diverse"
        elif diversity > 0.6:
            return "Moderately diverse"
        else:
            return "Focused taste"
