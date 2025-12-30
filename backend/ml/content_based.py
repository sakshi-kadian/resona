"""
Content-Based Filtering Helper

Provides genre-based similarity calculations.
This module will be used by Day 9 to enhance the hybrid recommendation engine.
"""

from typing import Dict, List, Set


def calculate_genre_similarity(user_genres: Set[str], track_genres: Set[str]) -> float:
    """
    Calculate Jaccard similarity between user and track genres
    
    Formula: similarity = |A ∩ B| / |A ∪ B|
    
    Args:
        user_genres: Set of user's top genres
        track_genres: Set of track's genres
        
    Returns:
        float: Similarity score (0-1)
    """
    if not user_genres or not track_genres:
        return 0.0
    
    intersection = user_genres & track_genres
    union = user_genres | track_genres
    
    return len(intersection) / len(union) if union else 0.0


def create_user_genre_profile(user_features: Dict) -> Set[str]:
    """
    Extract user's top genres from features
    
    Args:
        user_features: User's computed features
        
    Returns:
        set: User's top genres
    """
    genre_dist = user_features.get('genre_distribution', {})
    return set(genre_dist.keys())
