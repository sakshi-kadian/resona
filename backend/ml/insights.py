"""
ML Insights Module

Calculates advanced user insights:
1. Cluster Comparison (User vs Cluster Average)
2. Taste Evolution (Short vs Long Term)
3. Mathematical Diversity (Shannon Entropy)
"""

from typing import Dict, List, Any
import math
from collections import Counter


def calculate_genre_distribution_from_tracks(
    tracks: List[Dict], 
    artist_map: Dict[str, Dict]
) -> Dict[str, float]:
    """
    Calculate genre distribution from a list of tracks + artist data.
    """
    genre_counts = Counter()
    total_count = 0
    
    for track in tracks:
        for artist in track.get('artists', []):
            artist_id = artist.get('id')
            # Look up full artist info (with genres) from the artist map
            if artist_id and artist_id in artist_map:
                genres = artist_map[artist_id].get('genres', [])
                for genre in genres:
                    genre_counts[genre] += 1
                    total_count += 1
                    
    if total_count == 0:
        return {}
        
    return {k: v / total_count for k, v in genre_counts.items()}
    
def calculate_shannon_entropy(genre_distribution: Dict[str, float]) -> float:
    """
    Calculate Shannon Entropy for genre diversity.
    Formula: H = -sum(p_i * log2(p_i))
    
    Higher entropy = more complex/diverse taste.
    
    Args:
        genre_distribution: Dict of genre -> percentage (0-1) OR count
        
    Returns:
        float: Entropy score
    """
    if not genre_distribution:
        return 0.0
    
    values = list(genre_distribution.values())
    total = sum(values)
    
    if total == 0:
        return 0.0
        
    probabilities = []
    
    # If values are counts (sum > 1.01), normalize them
    if total > 1.01:
        probabilities = [v / total for v in values]
    else:
        probabilities = values
        
    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
            
    return round(entropy, 2)

def analyze_genre_evolution(
    short_term_genres: Dict[str, float],
    long_term_genres: Dict[str, float]
) -> Dict[str, Any]:
    """
    Analyze how user's taste has changed from Long Term -> Short Term.
    
    Args:
        short_term_genres: Current/Recent genre distribution
        long_term_genres: All-time genre distribution
        
    Returns:
        dict: Evolution insights (rising genres, falling genres, stability score)
    """
    rising = []
    falling = []
    
    all_genres = set(short_term_genres.keys()) | set(long_term_genres.keys())
    
    total_change = 0.0
    
    for genre in all_genres:
        st_pct = short_term_genres.get(genre, 0.0)
        lt_pct = long_term_genres.get(genre, 0.0)
        
        diff = st_pct - lt_pct
        total_change += abs(diff)
        
        if diff > 0.05: # Increased by more than 5%
            rising.append({"genre": genre, "change": diff})
        elif diff < -0.05: # Decreased by more than 5%
            falling.append({"genre": genre, "change": diff})
            
    # Stability Score: 1.0 - (Total Change / 2)
    # If total change is 0, stability is 100%. If total change is 2.0 (complete swap), stability is 0%.
    stability_score = max(0.0, 1.0 - (total_change / 2.0))
    
    return {
        "rising_genres": sorted(rising, key=lambda x: x['change'], reverse=True)[:3],
        "falling_genres": sorted(falling, key=lambda x: x['change'])[:3],
        "stability_score": round(stability_score, 2),
        "total_change_magnitude": round(total_change, 2)
    }

def calculate_cluster_deviation(
    user_features: Dict[str, Any],
    cluster_averages: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculate how the user deviates from their assigned cluster's average.
    
    Args:
        user_features: User's audio features (acousticness, energy, etc.)
        cluster_averages: Average features for the cluster (hardcoded baselines for now)
        
    Returns:
        dict: Deviation metrics
    """
    deviations = {}
    total_deviation = 0.0
    
    metrics = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'valence']
    
    for metric in metrics:
        user_val = user_features.get(metric, 0)
        cluster_val = cluster_averages.get(metric, 0)
        
        diff = user_val - cluster_val
        deviations[metric] = diff
        total_deviation += abs(diff)
        
    # Unique Score: Higher total deviation = more unique user within that cluster
    unique_score = min(1.0, total_deviation / len(metrics)) * 2 # Scale up a bit
    
    return {
        "deviations": deviations,
        "unique_score": round(unique_score, 2)
    }

# Hardcoded baselines for clusters (normally this would come from a DB of all users)
def calculate_mood_profile(user_features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate mood profile from audio features.
    
    Args:
        user_features: User's audio features
        
    Returns:
        dict: Mood profile with label and radar chart data
    """
    # Extract key mood indicators
    valence = user_features.get('valence', 0.5)  # Happiness (0-1)
    energy = user_features.get('energy', 0.5)    # Intensity (0-1)
    danceability = user_features.get('danceability', 0.5)
    acousticness = user_features.get('acousticness', 0.5)
    instrumentalness = user_features.get('instrumentalness', 0.5)
    
    # Determine mood label based on valence + energy
    if valence > 0.6 and energy > 0.6:
        mood_label = "Energetic & Happy"
        emoji = "🎉"
    elif valence > 0.6 and energy <= 0.6:
        mood_label = "Calm & Content"
        emoji = "😌"
    elif valence <= 0.6 and energy > 0.6:
        mood_label = "Intense & Passionate"
        emoji = "🔥"
    else:
        mood_label = "Melancholic & Reflective"
        emoji = "🌙"
    
    return {
        "mood_label": mood_label,
        "emoji": emoji,
        "radar_data": {
            "valence": round(valence, 2),
            "energy": round(energy, 2),
            "danceability": round(danceability, 2),
            "acousticness": round(acousticness, 2),
            "instrumentalness": round(instrumentalness, 2)
        }
    }


CLUSTER_BASELINES = {

    "Mainstream Pop Lovers": {
        "acousticness": 0.2, "danceability": 0.7, "energy": 0.7, "instrumentalness": 0.0, "valence": 0.6
    },
    "Indie Explorers": {
        "acousticness": 0.5, "danceability": 0.5, "energy": 0.5, "instrumentalness": 0.2, "valence": 0.4
    },
    "Niche Music Enthusiasts": {
        "acousticness": 0.4, "danceability": 0.4, "energy": 0.4, "instrumentalness": 0.3, "valence": 0.3
    },
    "Classic Music Fans": {
        "acousticness": 0.8, "danceability": 0.3, "energy": 0.3, "instrumentalness": 0.6, "valence": 0.2
    },
    "Genre Diverse Listeners": {
        "acousticness": 0.5, "danceability": 0.6, "energy": 0.6, "instrumentalness": 0.1, "valence": 0.5
    }
}
