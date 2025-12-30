"""
Explainability Helper

Adds simple explanations to recommendations showing why tracks were recommended.
"""

from typing import Dict, List


def add_explanation_to_track(track: Dict, user_cluster: str) -> Dict:
    """
    Add explanation to a single track
    
    Args:
        track: Track data with genre_score
        user_cluster: User's cluster label
        
    Returns:
        dict: Track with explanation added
    """
    # Get genre score if available
    genre_score = track.get('_genre_score', 0.0)
    genre_match_pct = int(genre_score * 100)
    
    # Get popularity
    popularity = track.get('popularity', 0)
    
    # Build explanation
    explanation_parts = []
    
    # Genre alignment
    if genre_score > 0:
        explanation_parts.append(f"✓ {genre_match_pct}% genre match")
    
    # Popularity indicator (always show this)
    if popularity >= 70:
        explanation_parts.append("✓ Popular hit")
    elif popularity >= 40:
        explanation_parts.append("✓ Moderately known")
    elif popularity > 0:
        explanation_parts.append("✓ Hidden gem")
    else:
        explanation_parts.append("✓ Recommended for you")
    
    # Combine
    track['explanation'] = " | ".join(explanation_parts) if explanation_parts else "✓ Recommended for you"
    
    return track


def add_explanations_to_recommendations(tracks: List[Dict], user_cluster: str) -> List[Dict]:
    """
    Add explanations to all recommended tracks
    
    Args:
        tracks: List of recommended tracks
        user_cluster: User's cluster label
        
    Returns:
        list: Tracks with explanations added
    """
    return [add_explanation_to_track(track, user_cluster) for track in tracks]
