"""
User Similarity Module

Calculate similarity between users based on their music features
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Any, Tuple

class SimilarityCalculator:
    """Calculate similarity between users"""
    
    def __init__(self):
        """Initialize similarity calculator"""
        pass
    
    def extract_feature_vector(self, features: Dict[str, Any]) -> np.ndarray:
        """
        Extract numerical feature vector from user features
        
        Args:
            features: User features dictionary
            
        Returns:
            numpy array: Feature vector
        """
        behavioral = features.get('behavioral', {})
        temporal = features.get('temporal', {})
        metadata = features.get('track_metadata', {})
        genre = features.get('genre', {})
        
        # Create feature vector (same as clustering)
        vector = [
            behavioral.get('repeat_rate', 0),
            behavioral.get('exploration_score', 0),
            behavioral.get('artist_diversity', 0),
            behavioral.get('track_loyalty', 0),
            behavioral.get('listening_consistency', 0),
            temporal.get('peak_listening_hour', 12) / 24.0,
            temporal.get('weekend_ratio', 0.5),
            temporal.get('listening_time_variance', 0.5),
            metadata.get('avg_popularity', 50) / 100.0,
            metadata.get('avg_duration_minutes', 3.5) / 10.0,
            genre.get('genre_diversity', 0.5),
            genre.get('genre_uniqueness', 0.5)
        ]
        
        return np.array(vector)
    
    def calculate_similarity(self, user1_features: Dict[str, Any], user2_features: Dict[str, Any]) -> float:
        """
        Calculate cosine similarity between two users
        
        Args:
            user1_features: First user's features
            user2_features: Second user's features
            
        Returns:
            float: Similarity score (0-1, higher = more similar)
        """
        # Extract feature vectors
        vec1 = self.extract_feature_vector(user1_features)
        vec2 = self.extract_feature_vector(user2_features)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
        
        return float(similarity)
    
    def find_similar_users(
        self, 
        target_user_features: Dict[str, Any],
        all_users_features: List[Dict[str, Any]],
        top_n: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Find most similar users to target user
        
        Args:
            target_user_features: Target user's features
            all_users_features: List of all users' features
            top_n: Number of similar users to return
            
        Returns:
            list: List of (user_id, similarity_score) tuples
        """
        target_vector = self.extract_feature_vector(target_user_features['features'])
        
        similarities = []
        for user_data in all_users_features:
            # Skip if same user
            if user_data.get('user_id') == target_user_features.get('user_id'):
                continue
            
            user_vector = self.extract_feature_vector(user_data['features'])
            similarity = cosine_similarity(
                target_vector.reshape(1, -1),
                user_vector.reshape(1, -1)
            )[0][0]
            
            similarities.append((user_data['user_id'], float(similarity)))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_n]
    
    def get_similarity_description(self, similarity_score: float) -> str:
        """
        Get human-readable description of similarity
        
        Args:
            similarity_score: Similarity score (0-1)
            
        Returns:
            str: Description
        """
        if similarity_score > 0.9:
            return "Almost identical music taste! 🎯"
        elif similarity_score > 0.8:
            return "Very similar music taste 🎵"
        elif similarity_score > 0.7:
            return "Similar music taste 👍"
        elif similarity_score > 0.6:
            return "Somewhat similar taste 🎶"
        else:
            return "Different music taste 🎭"

# Global similarity calculator
similarity_calc = SimilarityCalculator()
