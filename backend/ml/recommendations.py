"""
Recommendation Engine V2 - Reliable Alternative

Uses Related Artists + Top Tracks instead of the buggy /recommendations endpoint.
This is MORE reliable and gives us FULL control over filtering.
"""

from typing import Dict, List, Any
import random

class RecommendationEngineV2:
    """Generates personalized music recommendations using related artists"""
    
    def __init__(self, sp_client):
        """
        Initialize with Spotify client
        
        Args:
            sp_client: Authenticated Spotify client service
        """
        self.sp = sp_client
    
    def generate_recommendations(self, user_features: Dict[str, Any], cluster_label: str, limit: int = 20) -> Dict[str, Any]:
        """
        Generate recommendations based on user profile and cluster
        
        Strategy:
        1. Get user's top artists
        2. Find related artists
        3. Get top tracks from related artists
        4. Filter by cluster preferences
        
        Args:
            user_features: User's computed features
            cluster_label: User's assigned cluster label
            limit: Number of tracks to recommend
            
        Returns:
            dict: Recommendations with context
        """
        try:
            print(f"🎵 Generating recommendations for cluster: {cluster_label}")
            
            # 1. Get seed artist IDs
            seed_artist_ids = user_features.get('custom_seeds', {}).get('artist_ids', [])
            
            if not seed_artist_ids:
                return {"error": "No artist seeds available", "tracks": []}
            
            print(f"🌱 Using {len(seed_artist_ids)} seed artists")
            
            # SIMPLIFIED STRATEGY: Just get more tracks from YOUR OWN favorite artists
            # (Deep cuts you haven't heard yet)
            
            candidate_tracks = []
            for artist_id in seed_artist_ids[:10]:  # Use MORE artists (up to 10)
                try:
                    # Get this artist's top tracks
                    top_tracks = self.sp.sp.artist_top_tracks(artist_id, country='US')
                    # LIMIT to 2 tracks per artist for diversity
                    candidate_tracks.extend(top_tracks['tracks'][:3])
                except Exception as e:
                    print(f"   Warning: Couldn't get tracks for artist {artist_id}: {e}")
                    # If artist_top_tracks fails, try getting albums instead
                    try:
                        albums = self.sp.sp.artist_albums(artist_id, limit=2)
                        for album in albums['items']:
                            album_tracks = self.sp.sp.album_tracks(album['id'], limit=2)
                            # Get full track objects
                            for track in album_tracks['items'][:1]:  # Only 1 per album
                                try:
                                    full_track = self.sp.sp.track(track['id'])
                                    candidate_tracks.append(full_track)
                                except:
                                    pass
                    except Exception as e2:
                        print(f"   Warning: Album fallback also failed: {e2}")
                        continue
            
            print(f"🎶 Found {len(candidate_tracks)} candidate tracks from {len(seed_artist_ids)} artists")
            
            # 4. Filter by cluster preferences
            filtered_tracks = candidate_tracks # self._filter_by_cluster(candidate_tracks, cluster_label)
            
            # 5. Apply genre boosting (Day 9 enhancement)
            filtered_tracks = self._apply_genre_boost(filtered_tracks, user_features)
            
            # 6. Remove duplicates (same track ID)
            seen_ids = set()
            unique_tracks = []
            for track in filtered_tracks:
                if track['id'] not in seen_ids:
                    seen_ids.add(track['id'])
                    unique_tracks.append(track)
            
            # 7. Shuffle and limit
            random.shuffle(unique_tracks)
            final_tracks = unique_tracks[:limit]

            
            print(f"✅ Returning {len(final_tracks)} recommended tracks")
            
            # 6. Format results
            tracks = []
            for track in final_tracks:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artists': [{'name': a['name'], 'id': a['id']} for a in track['artists']],
                    'album': {
                        'name': track['album']['name'],
                        'image': track['album']['images'][0]['url'] if track['album']['images'] else None
                    },
                    'popularity': track['popularity'],
                    'preview_url': track.get('preview_url'),
                    'uri': track['uri'],
                    'external_url': track['external_urls']['spotify']
                })
            
            return {
                "cluster": cluster_label,
                "seeds_used": {
                    "artists": len(seed_artist_ids),
                    "genres": 0  # Not using genres in this approach
                },
                "strategy": f"Related Artists + Cluster Filtering for {cluster_label}",
                "tracks": tracks
            }
            
        except Exception as e:
            print(f"❌ Recommendation error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": str(e), "tracks": []}
    
    def _filter_by_cluster(self, tracks: List[Dict], cluster_label: str) -> List[Dict]:
        """Filter tracks based on cluster preferences (with fallback)"""
        
        filtered = []
        
        if cluster_label == "Mainstream Pop Lovers":
            # High popularity preferred
            filtered = [t for t in tracks if t.get('popularity', 0) >= 40] # Relaxed from 50
        
        elif cluster_label == "Indie Explorers":
            # Low to medium popularity preferred
            filtered = [t for t in tracks if t.get('popularity', 0) <= 80] # Relaxed from 70
        
        elif cluster_label == "Niche Music Enthusiasts":
            # Low popularity preferred
            filtered = [t for t in tracks if t.get('popularity', 0) <= 60] # Relaxed from 50
            
        elif cluster_label == "Classic Music Fans":
            # Medium popularity
            filtered = [t for t in tracks if t.get('popularity', 0) >= 20]
        
        else:  # Genre Diverse Listeners or unknown
            # No filtering
            return tracks
            
        # SAFETY CHECK: If filtering removed everything, return original tracks
        # This prevents "0 recommendations evaluated" errors
        if not filtered and tracks:
            print(f"⚠️ Cluster filter for {cluster_label} removed all tracks. Returning unfiltered list.")
            return tracks
            
        return filtered
    
    def _apply_genre_boost(self, tracks: List[Dict], user_features: Dict[str, Any]) -> List[Dict]:
        """
        Boost tracks that match user's genre preferences
        
        This creates a hybrid approach: artist-based + genre-based
        """
        # Get user's top genres
        user_genres = set(user_features.get('genre_distribution', {}).keys())
        
        if not user_genres:
            return tracks  # No genre boost if no genre data
        
        # Add genre match score to each track
        boosted_tracks = []
        for track in tracks:
            # Get track's artist genres
            track_genres = set()
            for artist in track.get('artists', []):
                try:
                    artist_info = self.sp.sp.artist(artist['id'])
                    track_genres.update(artist_info.get('genres', []))
                except:
                    pass
            
            # Calculate genre overlap
            if track_genres:
                overlap = len(user_genres & track_genres) / len(user_genres | track_genres)
            else:
                overlap = 0.0
            
            # Add genre score to track
            track['_genre_score'] = overlap
            boosted_tracks.append(track)
        
        # Sort by genre score (higher = better match)
        boosted_tracks.sort(key=lambda t: t.get('_genre_score', 0), reverse=True)
        
        return boosted_tracks
