"""
Spotify Data Client

Wrapper around Spotipy for fetching user data from Spotify API
"""

import spotipy
from typing import List, Dict, Any, Optional
from datetime import datetime

class SpotifyDataClient:
    """Client for fetching user data from Spotify"""
    
    def __init__(self, access_token: str):
        """
        Initialize Spotify client with user's access token
        
        Args:
            access_token: User's Spotify access token
        """
        self.access_token = access_token
        self.sp = spotipy.Spotify(auth=access_token)
    
    def get_top_tracks(self, time_range: str = "medium_term", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's top tracks
        
        Args:
            time_range: Time range for top tracks
                - short_term: ~4 weeks
                - medium_term: ~6 months (default)
                - long_term: several years
            limit: Number of tracks to fetch (max 50)
            
        Returns:
            List of track objects
        """
        results = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)
        return results['items']
    
    def get_recently_played(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's recently played tracks
        
        Args:
            limit: Number of tracks to fetch (max 50)
            
        Returns:
            List of recently played track objects
        """
        results = self.sp.current_user_recently_played(limit=limit)
        return results['items']
    
    
    def get_artist_info(self, artist_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get artist information including genres
        
        Args:
            artist_ids: List of Spotify artist IDs
            
        Returns:
            List of artist objects
        """
        # Spotify API allows max 50 artists per request
        all_artists = []
        
        for i in range(0, len(artist_ids), 50):
            batch = artist_ids[i:i + 50]
            artists = self.sp.artists(batch)
            all_artists.extend(artists['artists'])
        
        return all_artists
    
    def get_user_profile(self) -> Dict[str, Any]:
        """
        Get current user's profile
        
        Returns:
            User profile object
        """
        return self.sp.current_user()
    
    def get_user_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's playlists
        
        Args:
            limit: Number of playlists to fetch
            
        Returns:
            List of playlist objects
        """
        results = self.sp.current_user_playlists(limit=limit)
        return results['items']
    
    def get_saved_tracks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's saved (liked) tracks
        
        Args:
            limit: Number of tracks to fetch
            
        Returns:
            List of saved track objects
        """
        results = self.sp.current_user_saved_tracks(limit=limit)
        return results['items']
    
    def get_saved_tracks_count(self) -> int:
        """Get total number of saved tracks"""
        try:
            results = self.sp.current_user_saved_tracks(limit=1)
            return results['total']
        except Exception as e:
            print(f"⚠️ Could not fetch saved tracks count: {str(e)}")
            return 0

    def get_followed_artists_count(self) -> int:
        """Get total number of followed artists"""
        try:
            results = self.sp.current_user_followed_artists(limit=1)
            return results['artists']['total']
        except Exception as e:
            print(f"⚠️ Could not fetch followed artists count: {str(e)}")
            return 0

    def fetch_all_user_data(self) -> Dict[str, Any]:
        """
        Fetch all required user data in one call
        
        Returns:
            Dictionary containing all user data:
            - profile: User profile
            - top_tracks_short: Top tracks (4 weeks)
            - top_tracks_medium: Top tracks (6 months)
            - top_tracks_long: Top tracks (several years)
            - recently_played: Recently played tracks
            - artists: Artist information with genres
            - total_liked_songs: Count of liked songs
            - total_followed_artists: Count of followed artists
        """
        print("📊 Fetching user data from Spotify...")
        
        # Get user profile
        profile = self.get_user_profile()
        
        # Get top tracks for different time ranges
        top_tracks_short = self.get_top_tracks(time_range="short_term", limit=50)
        top_tracks_medium = self.get_top_tracks(time_range="medium_term", limit=50)
        top_tracks_long = self.get_top_tracks(time_range="long_term", limit=50)
        
        # Get recently played tracks
        recently_played = self.get_recently_played(limit=50)

        # Get counts
        total_liked = self.get_saved_tracks_count()
        total_followed = self.get_followed_artists_count()
        
        # Combine all tracks
        all_tracks = []
        all_tracks.extend(top_tracks_short)
        all_tracks.extend(top_tracks_medium)
        all_tracks.extend(top_tracks_long)
        all_tracks.extend([item['track'] for item in recently_played])
        
        # Get unique artist IDs
        artist_ids = []
        for track in all_tracks:
            if track and track.get('artists'):
                artist_ids.extend([artist['id'] for artist in track['artists']])
        artist_ids = list(set(artist_ids))
        
        # Get artist information
        print(f"🎤 Fetching information for {len(artist_ids)} artists...")
        artists = self.get_artist_info(artist_ids)
        
        print("✅ All data fetched successfully!")
        
        return {
            "profile": profile,
            "top_tracks_short": top_tracks_short,
            "top_tracks_medium": top_tracks_medium,
            "top_tracks_long": top_tracks_long,
            "recently_played": recently_played,
            "artists": artists,
            "total_liked_songs": total_liked,
            "total_followed_artists": total_followed,
            "fetched_at": datetime.utcnow().isoformat()
        }
