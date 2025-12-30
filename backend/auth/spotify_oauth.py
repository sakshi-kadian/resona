"""
Spotify OAuth 2.0 Authentication Module

This module handles the OAuth 2.0 flow with Spotify:
1. Redirects users to Spotify for authorization
2. Handles the callback with authorization code
3. Exchanges code for access token
4. Generates JWT for session management
"""

from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from config import settings

class SpotifyAuthManager:
    """Manages Spotify OAuth 2.0 authentication flow"""
    
    def __init__(self):
        self.client_id = settings.spotify_client_id
        self.client_secret = settings.spotify_client_secret
        self.redirect_uri = settings.spotify_redirect_uri
        
        # Scopes we need for Resona
        self.scope = " ".join([
            "user-read-email",
            "user-read-private",
            "user-top-read",
            "user-read-recently-played",
            "user-library-read",
            "user-follow-read",
            "playlist-read-private",
            "playlist-read-collaborative"
        ])
        
        # Initialize Spotify OAuth
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=None  # Don't cache tokens to file
        )
    
    def get_authorization_url(self) -> str:
        """
        Generate Spotify authorization URL
        
        Returns:
            str: URL to redirect user to for Spotify login
        """
        auth_url = self.sp_oauth.get_authorize_url()
        return auth_url
    
    def get_access_token(self, code: str) -> dict:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Spotify callback
            
        Returns:
            dict: Token info containing access_token, refresh_token, expires_at
            
        Raises:
            HTTPException: If token exchange fails
        """
        try:
            token_info = self.sp_oauth.get_access_token(code, as_dict=True)
            return token_info
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get access token: {str(e)}"
            )
    
    def get_user_info(self, access_token: str) -> dict:
        """
        Get Spotify user profile information
        
        Args:
            access_token: Spotify access token
            
        Returns:
            dict: User profile data (id, email, display_name, etc.)
        """
        sp = spotipy.Spotify(auth=access_token)
        user_info = sp.current_user()
        return user_info
    
    def create_jwt_token(self, user_id: str, spotify_access_token: str, spotify_refresh_token: str) -> str:
        """
        Create JWT token for session management
        
        Args:
            user_id: Spotify user ID
            spotify_access_token: Spotify API access token
            spotify_refresh_token: Spotify API refresh token
            
        Returns:
            str: Encoded JWT token
        """
        expiration = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
        
        payload = {
            "user_id": user_id,
            "spotify_access_token": spotify_access_token,
            "spotify_refresh_token": spotify_refresh_token,
            "exp": expiration,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        
        return token
    
    def verify_jwt_token(self, token: str) -> dict:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
            
        Returns:
            dict: Decoded token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

# Global instance
auth_manager = SpotifyAuthManager()
