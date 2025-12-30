"""
Storage Module

Handles saving and loading user data and features to/from JSON files
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class DataStorage:
    """Manages storage of user data and features"""
    
    def __init__(self, storage_dir: str = "data/users"):
        """
        Initialize storage
        
        Args:
            storage_dir: Directory to store user data
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_user_dir(self, user_id: str) -> Path:
        """Get directory for specific user"""
        user_dir = self.storage_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def save_user_data(self, user_id: str, data: Dict[str, Any]) -> str:
        """
        Save user's Spotify data
        
        Args:
            user_id: Spotify user ID
            data: User data from Spotify
            
        Returns:
            str: Path to saved file
        """
        user_dir = self._get_user_dir(user_id)
        
        # Add metadata
        data['saved_at'] = datetime.utcnow().isoformat()
        data['user_id'] = user_id
        
        # Save to file
        filepath = user_dir / "spotify_data.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved user data to {filepath}")
        return str(filepath)
    
    def load_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Load user's Spotify data
        
        Args:
            user_id: Spotify user ID
            
        Returns:
            dict: User data or None if not found
        """
        user_dir = self._get_user_dir(user_id)
        filepath = user_dir / "spotify_data.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded user data from {filepath}")
        return data
    
    def save_features(self, user_id: str, features: Dict[str, Any], version: str = "1.0") -> str:
        """
        Save computed features
        
        Args:
            user_id: Spotify user ID
            features: Computed features
            version: Feature version
            
        Returns:
            str: Path to saved file
        """
        user_dir = self._get_user_dir(user_id)
        
        # Add metadata
        feature_data = {
            "user_id": user_id,
            "version": version,
            "computed_at": datetime.utcnow().isoformat(),
            "features": features
        }
        
        # Save to file
        filepath = user_dir / f"features_v{version}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feature_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved features to {filepath}")
        return str(filepath)
    
    def load_features(self, user_id: str, version: str = "1.0") -> Optional[Dict[str, Any]]:
        """
        Load computed features
        
        Args:
            user_id: Spotify user ID
            version: Feature version
            
        Returns:
            dict: Features or None if not found
        """
        user_dir = self._get_user_dir(user_id)
        filepath = user_dir / f"features_v{version}.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Loaded features from {filepath}")
        return data
    
    def data_exists(self, user_id: str) -> bool:
        """Check if user data exists"""
        user_dir = self._get_user_dir(user_id)
        return (user_dir / "spotify_data.json").exists()
    
    def features_exist(self, user_id: str, version: str = "1.0") -> bool:
        """Check if features exist"""
        user_dir = self._get_user_dir(user_id)
        return (user_dir / f"features_v{version}.json").exists()
    
    def get_data_age(self, user_id: str) -> Optional[float]:
        """
        Get age of cached data in hours
        
        Args:
            user_id: Spotify user ID
            
        Returns:
            float: Age in hours or None if no data
        """
        data = self.load_user_data(user_id)
        if not data or 'saved_at' not in data:
            return None
        
        saved_at = datetime.fromisoformat(data['saved_at'])
        age = (datetime.utcnow() - saved_at).total_seconds() / 3600
        
        return age
    
    def should_refresh(self, user_id: str, max_age_hours: float = 24) -> bool:
        """
        Check if data should be refreshed
        
        Args:
            user_id: Spotify user ID
            max_age_hours: Maximum age before refresh
            
        Returns:
            bool: True if should refresh
        """
        if not self.data_exists(user_id):
            return True
        
        age = self.get_data_age(user_id)
        if age is None:
            return True
        
        return age > max_age_hours

# Global storage instance
storage = DataStorage()
