"""
Genre Features Module

Extracts features from genre data:
- Genre distribution
- Genre diversity (entropy)
- Top genres
- Genre clustering
"""

from typing import Dict, List, Any
from collections import Counter
import numpy as np

class GenreFeatures:
    """Extract features from genre data"""
    
    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize with user data
        
        Args:
            user_data: Complete user data from Spotify
        """
        self.user_data = user_data
        self.artists = user_data.get('artists', [])
    
    def get_all_genres(self) -> List[str]:
        """
        Get all genres from user's artists
        
        Returns:
            list: All genres
        """
        all_genres = []
        for artist in self.artists:
            if artist.get('genres'):
                all_genres.extend(artist['genres'])
        return all_genres
    
    def calculate_genre_distribution(self) -> Dict[str, int]:
        """
        Calculate distribution of genres
        
        Returns:
            dict: Genre counts
        """
        all_genres = self.get_all_genres()
        genre_counts = Counter(all_genres)
        
        # Return top 10 genres
        return dict(genre_counts.most_common(10))
    
    def calculate_genre_diversity(self) -> float:
        """
        Calculate genre diversity using entropy
        
        Returns:
            float: Genre diversity score (0-1, higher = more diverse)
        """
        all_genres = self.get_all_genres()
        
        if not all_genres:
            return 0.0
        
        # Calculate genre probabilities
        genre_counts = Counter(all_genres)
        total = len(all_genres)
        probabilities = [count / total for count in genre_counts.values()]
        
        # Calculate Shannon entropy
        entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
        
        # Normalize to 0-1 (max entropy for 10 genres is ~3.32)
        max_entropy = np.log2(min(len(genre_counts), 10))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return round(normalized_entropy, 3)
    
    def get_top_genres(self, n: int = 5) -> List[str]:
        """
        Get top N genres
        
        Args:
            n: Number of top genres to return
            
        Returns:
            list: Top genres
        """
        genre_dist = self.calculate_genre_distribution()
        return list(genre_dist.keys())[:n]
    
    def calculate_genre_uniqueness(self) -> float:
        """
        Calculate how unique user's genre taste is
        
        Returns:
            float: Uniqueness score (0-1, higher = more unique/niche)
        """
        all_genres = self.get_all_genres()
        
        if not all_genres:
            return 0.5
        
        # Count unique genres
        unique_genres = len(set(all_genres))
        
        # More unique genres = more niche taste
        # Normalize: 1-5 genres = mainstream, 20+ = very niche
        uniqueness = min(unique_genres / 20, 1.0)
        
        return round(uniqueness, 3)
    
    def extract_all_features(self) -> Dict[str, Any]:
        """
        Extract all genre features
        
        Returns:
            dict: All genre features
        """
        return {
            "genre_distribution": self.calculate_genre_distribution(),
            "genre_diversity": self.calculate_genre_diversity(),
            "top_genres": self.get_top_genres(),
            "genre_uniqueness": self.calculate_genre_uniqueness(),
            "total_unique_genres": len(set(self.get_all_genres()))
        }
