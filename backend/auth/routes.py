"""
Authentication routes for Spotify OAuth 2.0

Endpoints:
- GET /auth/login - Redirects to Spotify for authorization
- GET /auth/callback - Handles OAuth callback from Spotify
- GET /auth/me - Get current user info (protected route)
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import RedirectResponse
from typing import Optional
from auth.spotify_oauth import auth_manager
from config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/login")
def login():
    """
    Redirect user to Spotify for authorization
    
    Returns:
        RedirectResponse: Redirects to Spotify login page
    """
    auth_url = auth_manager.get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def callback(code: Optional[str] = None, error: Optional[str] = None):
    """
    Handle OAuth callback from Spotify
    
    Args:
        code: Authorization code from Spotify
        error: Error message if authorization failed
        
    Returns:
        RedirectResponse: Redirects to frontend with JWT token
    """
    # Check for errors
    if error:
        # Redirect to frontend with error
        return RedirectResponse(
            url=f"{settings.frontend_url}/?error={error}"
        )
    
    if not code:
        raise HTTPException(
            status_code=400,
            detail="No authorization code provided"
        )
    
    # Exchange code for access token
    token_info = auth_manager.get_access_token(code)
    
    # Get user info from Spotify
    user_info = auth_manager.get_user_info(token_info['access_token'])
    
    # Create JWT token
    jwt_token = auth_manager.create_jwt_token(
        user_id=user_info['id'],
        spotify_access_token=token_info['access_token'],
        spotify_refresh_token=token_info['refresh_token']
    )
    
    # Redirect to frontend with token
    return RedirectResponse(
        url=f"{settings.frontend_url}/auth?token={jwt_token}"
    )

@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Get current user information (protected route)
    
    Args:
        authorization: Bearer token from Authorization header
        
    Returns:
        dict: User information
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )
    
    # Extract token
    token = authorization.replace("Bearer ", "")
    
    # Verify JWT token
    payload = auth_manager.verify_jwt_token(token)
    
    # Get user info from Spotify
    user_info = auth_manager.get_user_info(payload['spotify_access_token'])
    
    return {
        "user_id": payload['user_id'],
        "display_name": user_info.get('display_name'),
        "email": user_info.get('email'),
        "profile_image": user_info.get('images', [{}])[0].get('url') if user_info.get('images') else None
    }
