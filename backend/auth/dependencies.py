"""
Dependencies for protected routes

This module provides FastAPI dependencies for:
- Extracting and validating JWT tokens
- Getting current user information
- Accessing Spotify API with user's token
"""

from fastapi import Depends, HTTPException, Header, status
from typing import Optional
from auth.spotify_oauth import auth_manager
import spotipy

def get_current_user_token(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependency to extract and verify JWT token from Authorization header
    
    Args:
        authorization: Bearer token from Authorization header
        
    Returns:
        dict: Decoded JWT payload containing user_id and spotify tokens
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token
    token = authorization.replace("Bearer ", "")
    
    # Verify and decode JWT
    payload = auth_manager.verify_jwt_token(token)
    
    return payload

def get_spotify_client(token_data: dict = Depends(get_current_user_token)) -> spotipy.Spotify:
    """
    Dependency to get authenticated Spotify client for current user
    
    Args:
        token_data: JWT payload from get_current_user_token
        
    Returns:
        spotipy.Spotify: Authenticated Spotify client
    """
    sp = spotipy.Spotify(auth=token_data['spotify_access_token'])
    return sp

def get_current_user_id(token_data: dict = Depends(get_current_user_token)) -> str:
    """
    Dependency to get current user's Spotify ID
    
    Args:
        token_data: JWT payload from get_current_user_token
        
    Returns:
        str: User's Spotify ID
    """
    return token_data['user_id']
