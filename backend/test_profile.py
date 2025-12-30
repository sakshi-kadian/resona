"""
Test script for Day 3 - Data Fetching

This script tests the /api/profile endpoint
Run this after logging in to verify data fetching works

Usage:
    1. Log in through the frontend (http://localhost:3000)
    2. Copy your JWT token from browser localStorage
    3. Replace YOUR_TOKEN_HERE with your actual token
    4. Run: python test_profile.py
"""

import httpx
import json

# Replace this with your actual JWT token from localStorage
TOKEN = "YOUR_TOKEN_HERE"

API_BASE_URL = "http://localhost:8000"

def test_profile():
    """Test the /api/profile endpoint"""
    
    print("🧪 Testing /api/profile endpoint...\n")
    
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    try:
        # Test profile summary first (faster)
        print("📊 Fetching profile summary...")
        response = httpx.get(f"{API_BASE_URL}/api/profile/summary", headers=headers, timeout=30.0)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Profile Summary:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Top Tracks: {data['top_tracks_count']}")
            print(f"   Top Artists: {data['top_artists_count']}")
            print(f"   Unique Genres: {data['unique_genres_count']}")
            print(f"   Top Genres: {', '.join(data['top_genres'])}\n")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}\n")
            return
        
        # Test full profile (slower)
        print("📊 Fetching complete profile (this may take 10-30 seconds)...")
        response = httpx.get(f"{API_BASE_URL}/api/profile", headers=headers, timeout=60.0)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Complete Profile Fetched!")
            print(f"\n📈 Data Summary:")
            print(f"   Top Tracks (Short): {len(data['top_tracks_short'])}")
            print(f"   Top Tracks (Medium): {len(data['top_tracks_medium'])}")
            print(f"   Top Tracks (Long): {len(data['top_tracks_long'])}")
            print(f"   Recently Played: {len(data['recently_played'])}")
            print(f"   Audio Features: {len(data['audio_features'])}")
            print(f"   Artists: {len(data['artists'])}")
            print(f"   Fetched At: {data['fetched_at']}")
            
            # Show sample track
            if data['top_tracks_medium']:
                track = data['top_tracks_medium'][0]
                print(f"\n🎵 Your #1 Track (Medium Term):")
                print(f"   {track['name']} by {track['artists'][0]['name']}")
            
            # Show sample audio features
            if data['audio_features']:
                features = data['audio_features'][0]
                print(f"\n🎼 Sample Audio Features:")
                print(f"   Valence: {features['valence']:.2f}")
                print(f"   Energy: {features['energy']:.2f}")
                print(f"   Danceability: {features['danceability']:.2f}")
                print(f"   Tempo: {features['tempo']:.1f} BPM")
            
            print("\n✅ All tests passed! Day 3 complete!")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. Backend is running (python app.py)")
        print("2. You've logged in and copied your token")
        print("3. Token is not expired")

if __name__ == "__main__":
    if TOKEN == "YOUR_TOKEN_HERE":
        print("❌ Please replace YOUR_TOKEN_HERE with your actual JWT token")
        print("\nHow to get your token:")
        print("1. Open http://localhost:3000 in browser")
        print("2. Log in with Spotify")
        print("3. Open browser DevTools (F12)")
        print("4. Go to Application > Local Storage > http://localhost:3000")
        print("5. Copy the value of 'resona_token'")
        print("6. Paste it in this script")
    else:
        test_profile()
