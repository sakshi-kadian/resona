"""
Spotify API test script

This script tests the Spotify API connection using Client Credentials flow.
Run this to verify your Spotify Developer credentials are working.

Usage:
    python test_spotify.py
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_spotify_connection():
    """Test Spotify API connection"""
    
    print("🎵 Testing Spotify API Connection...\n")
    
    # Get credentials from environment
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ ERROR: Spotify credentials not found in .env file")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your Spotify Client ID and Client Secret")
        print("3. Get credentials from: https://developer.spotify.com/dashboard")
        return False
    
    try:
        # Initialize Spotify client
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))
        
        # Test: Get a popular track
        track_id = "3n3Ppam7vgaVa1iaRUc9Lp"  # Mr. Brightside by The Killers
        track = sp.track(track_id)
        
        print("✅ Spotify API Connection Successful!\n")
        print(f"Test Track: {track['name']}")
        print(f"Artist: {track['artists'][0]['name']}")
        print(f"Album: {track['album']['name']}")
        print(f"Popularity: {track['popularity']}/100")
        
        # Test: Get audio features
        audio_features = sp.audio_features([track_id])[0]
        print(f"\nAudio Features:")
        print(f"  Valence (happiness): {audio_features['valence']:.2f}")
        print(f"  Energy: {audio_features['energy']:.2f}")
        print(f"  Danceability: {audio_features['danceability']:.2f}")
        print(f"  Tempo: {audio_features['tempo']:.1f} BPM")
        
        print("\n✅ All tests passed! Your Spotify API is ready to use.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}\n")
        print("Please check:")
        print("1. Your Client ID and Client Secret are correct")
        print("2. You have internet connection")
        print("3. Spotify API is accessible")
        return False

if __name__ == "__main__":
    test_spotify_connection()
