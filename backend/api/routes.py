"""
API routes for user profile and data

Endpoints:
- GET /api/profile - Get complete user profile with all Spotify data
"""

from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user_token
from services.spotify_client import SpotifyDataClient
from storage.data_storage import storage

router = APIRouter(prefix="/api", tags=["Profile"])

@router.get("/profile")
def get_user_profile(token_data: dict = Depends(get_current_user_token), force_refresh: bool = False):
    """
    Get complete user profile with all Spotify data AND calculated statistics
    
    Returns:
        dict: Complete user profile data with calculated stats
    """
    try:
        user_id = token_data['user_id']
        user_data = None
        
        # Check if we should use cached data
        if not force_refresh and storage.data_exists(user_id):
            age = storage.get_data_age(user_id)
            if age is not None and age < 24:  # Cache for 24 hours
                print(f"Using cached data (age: {age:.1f} hours)")
                user_data = storage.load_user_data(user_id)
                # Check if new fields exist (if not, force refresh)
                if 'total_liked_songs' not in user_data or 'total_followed_artists' not in user_data:
                    print("Cached data missing new fields, forcing refresh...")
                    user_data = None
                else:
                    user_data['from_cache'] = True
                    user_data['cache_age_hours'] = round(age, 2)
        
        if not user_data:
            # Fetch fresh data from Spotify
            print("Fetching fresh data from Spotify...")
            spotify_client = SpotifyDataClient(token_data['spotify_access_token'])
            user_data = spotify_client.fetch_all_user_data()
            
            # Add user ID from token
            user_data['user_id'] = user_id
            user_data['from_cache'] = False
            
            # Save to storage
            storage.save_user_data(user_id, user_data)
            
        # Enrich with calculated statistics
        stats = _calculate_statistics(user_data)
        user_data.update(stats)
        
        return user_data
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        
        print(f"Error fetching profile: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch Spotify data: {str(e)}"
        )

@router.get("/statistics")
def get_user_statistics(token_data: dict = Depends(get_current_user_token)):
    """
    Get meaningful listening statistics
    
    Returns:
        dict: Listening statistics (songs this month, unique artists, top genre, etc.)
    """
    try:
        # Get user data (will use cache if available)
        user_data = get_user_profile(token_data, force_refresh=False)
        
        # Stats are already added by get_user_profile now, but we'll recalculate/return strict subset if needed
        # Or just return the stats part. Since get_user_profile already adds them, we can just extract them
        # or call _calculate_statistics again.
        return _calculate_statistics(user_data)
        
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        
        print(f"Error calculating statistics: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate statistics: {str(e)}"
        )

def _calculate_statistics(user_data: dict) -> dict:
    """Helper to calculate statistics from user data"""
    from collections import Counter
    
    # Get all unique tracks from different time ranges
    all_track_ids = set()
    all_artist_ids = set()
    all_genres = []
    
    # From top tracks (long term = ~several years / all time)
    if 'top_tracks_long' in user_data:
        for track in user_data['top_tracks_long']:
            all_track_ids.add(track['id'])
            for artist in track.get('artists', []):
                all_artist_ids.add(artist['id'])
    
    # From recently played (last 50 tracks)
    recent_track_ids = set()
    if 'recently_played' in user_data:
        for item in user_data['recently_played']:
            track = item.get('track', {})
            recent_track_ids.add(track['id'])
            for artist in track.get('artists', []):
                all_artist_ids.add(artist['id'])
    
    # Get genres from user artists (filtered by long term top artists for accuracy)
    # Get genres from user artists (filtered by long term top artists for accuracy)
    # create artist map first
    artist_map = {a['id']: a for a in user_data.get('artists', [])}
    
    relevant_genres = []
    if 'top_tracks_long' in user_data:
        for track in user_data['top_tracks_long']:
             for artist_simple in track.get('artists', []):
                 artist_full = artist_map.get(artist_simple['id'])
                 if artist_full:
                     relevant_genres.extend(artist_full.get('genres', []))
    
    genre_counts = Counter(relevant_genres)
    if not genre_counts and 'artists' in user_data: # Fallback using all artists unweighted if top tracks have no genres
             for artist in user_data['artists']:
                 relevant_genres.extend(artist.get('genres', []))
             genre_counts = Counter(relevant_genres)


    top_genres_data = []
    total_genre_count = sum(genre_counts.values())
    for genre, count in genre_counts.most_common(10):
        top_genres_data.append({
            "name": genre,
            "count": count,
            "percent": round((count / total_genre_count) * 100) if total_genre_count > 0 else 0
        })
    top_genre = top_genres_data[0]['name'] if top_genres_data else "Various"

    # 2. Top Artists (Rich Data with Images)
    artist_id_counts = Counter()
    if 'top_tracks_long' in user_data:
        for track in user_data['top_tracks_long']:
            for artist in track.get('artists', []):
                artist_id_counts[artist['id']] += 1
    
    # Create a map for artist details from the 'artists' list
    artist_details_map = {a['id']: a for a in user_data.get('artists', [])}
    
    top_artists_data = []
    for artist_id, count in artist_id_counts.most_common(5):
        artist_info = artist_details_map.get(artist_id)
        if artist_info:
            image_url = artist_info['images'][0]['url'] if artist_info.get('images') else None
            top_artists_data.append({
                "name": artist_info['name'],
                "id": artist_id,
                "count": count,
                "image": image_url
            })
    
    top_artist = top_artists_data[0]['name'] if top_artists_data else "Unknown"

    # 3. Top Tracks (Rich Data)
    top_tracks_data = []
    if 'top_tracks_long' in user_data:
        for track in user_data['top_tracks_long'][:6]:
            image_url = track['album']['images'][0]['url'] if track['album'].get('images') else None
            top_tracks_data.append({
                "name": track['name'],
                "artist": track['artists'][0]['name'] if track['artists'] else "Unknown",
                "image": image_url,
                "id": track['id']
            })

    # 4. Estimate Total Listening Time (All Time Proxy)
    # We use total_liked_songs as a proxy for library size * average song duration (3.5 mins)
    total_liked = user_data.get('total_liked_songs', 0)
    avg_duration_hours = (3.5 * 60) / 3600 # ~0.0583 hours per song
    estimated_total_hours = round(total_liked * avg_duration_hours, 1)

    return {
        "total_unique_tracks": len(all_track_ids),
        "recent_tracks_count": len(recent_track_ids),
        "unique_artists": len(all_artist_ids),
        "top_genre": top_genre,
        "top_artist": top_artist,
        "total_liked_songs": total_liked,
        "total_followed_artists": user_data.get('total_followed_artists', 0),
        "estimated_total_hours": estimated_total_hours,
        "total_genres": len(set(all_genres)),
        "top_artists_list": top_artists_data,
        "top_genres_list": top_genres_data,
        "top_tracks_list": top_tracks_data
    }
        



@router.get("/profile/summary")
def get_profile_summary(token_data: dict = Depends(get_current_user_token)):
    """
    Get quick summary of user profile
    
    Returns:
        dict: Summary statistics
    """
    spotify_client = SpotifyDataClient(token_data['spotify_access_token'])
    
    # Get top tracks
    top_tracks = spotify_client.get_top_tracks(time_range="medium_term", limit=10)
    
    # Get unique artists
    artist_ids = list(set([artist['id'] for track in top_tracks for artist in track['artists']]))
    artists = spotify_client.get_artist_info(artist_ids)
    
    # Get unique genres
    all_genres = []
    for artist in artists:
        all_genres.extend(artist.get('genres', []))
    unique_genres = list(set(all_genres))
    
    return {
        "user_id": token_data['user_id'],
        "top_tracks_count": len(top_tracks),
        "top_artists_count": len(artists),
        "unique_genres_count": len(unique_genres),
        "top_genres": unique_genres[:5] if unique_genres else []
    }

@router.get("/features")
def get_user_features(token_data: dict = Depends(get_current_user_token), force_refresh: bool = False):
    """
    Compute ML features from user's Spotify data
    
    Returns:
        dict: Complete feature set
    """
    try:
        user_id = token_data['user_id']
        
        # Check if we have cached features
        if not force_refresh and storage.features_exist(user_id):
            print("Using cached features")
            cached_features = storage.load_features(user_id)
            cached_features['from_cache'] = True
            return cached_features
        
        # Get user data (will use cache if available)
        user_data = get_user_profile(token_data, force_refresh=False)
        
        # Extract features
        from features.user_features import UserFeatures
        feature_extractor = UserFeatures(user_data)
        
        features = feature_extractor.extract_all_features()
        summary = feature_extractor.get_feature_summary()
        
        result = {
            "user_id": user_id,
            "features": features,
            "summary": summary,
            "computed_at": user_data.get('fetched_at'),
            "from_cache": False
        }
        
        # Save features to storage
        storage.save_features(user_id, result)
        
        return result
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        
        print(f"Error computing features: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compute features: {str(e)}"
        )

@router.get("/cluster")
def get_user_cluster(token_data: dict = Depends(get_current_user_token)):
    """
    Get user's music taste cluster
    
    Returns:
        dict: Cluster information
    """
    try:
        user_id = token_data['user_id']
        
        # Get user features
        user_features_data = get_user_features(token_data, force_refresh=False)
        
        # For now, return a demo cluster (we'll train the model later with multiple users)
        from ml.clustering import clusterer
        
        # Predict cluster
        cluster_id, cluster_label = clusterer.predict_cluster(user_features_data['features'])
        cluster_description = clusterer.get_cluster_description(cluster_id)
        
        return {
            "user_id": user_id,
            "cluster_id": cluster_id,
            "cluster_label": cluster_label,
            "description": cluster_description,
            "total_clusters": clusterer.n_clusters
        }
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        
        print(f"Error predicting cluster: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to predict cluster: {str(e)}"
        )


@router.get("/recommendations")
def get_recommendations(
    token_data: dict = Depends(get_current_user_token),
    limit: int = 20
):
    """
    Get personalized music recommendations based on ML cluster
    
    Args:
        limit: Number of tracks to recommend
        
    Returns:
        dict: Recommendation results
    """
    try:
        user_id = token_data['user_id']
        
        # 1. Get User Profile (for Artist IDs seed)
        # We need fresh or cached profile data to get real Artist IDs 
        # because the features JSON only has stats, not IDs.
        user_data = get_user_profile(token_data, force_refresh=False)
        
        # 2. Get User Features (for Cluster & Genre seeds)
        # Calculate or load features
        from features.user_features import UserFeatures
        if storage.features_exist(user_id):
            user_features_data = storage.load_features(user_id)
        else:
            # Compute if missing
            feature_extractor = UserFeatures(user_data)
            feats = feature_extractor.extract_all_features()
            summary = feature_extractor.get_feature_summary()
            user_features_data = {"features": feats, "summary": summary}
            
        # 3. Determine Cluster
        from ml.clustering import clusterer
        cluster_id, cluster_label = clusterer.predict_cluster(user_features_data['features'])
        
        # 4. Initialize Recommendation Engine V2 (uses Related Artists instead of /recommendations)
        from ml.recommendations import RecommendationEngineV2
        # We need a fresh Spotify client
        sp_client = SpotifyDataClient(token_data['spotify_access_token'])
        engine = RecommendationEngineV2(sp_client)
        
        # 5. Extract top artist IDs by FREQUENCY (not just first tracks)
        from collections import Counter
        
        artist_counts = Counter()
        if 'top_tracks_medium' in user_data:
            for track in user_data['top_tracks_medium']:
                track_artists = track.get('artists', [])
                for artist in track_artists:
                    artist_id = artist.get('id')
                    if artist_id and len(artist_id) == 22:  # Valid Spotify ID
                        artist_counts[artist_id] += 1
        
        # Get top 10 artists by frequency
        top_artist_ids = [artist_id for artist_id, count in artist_counts.most_common(10)]
        
        print(f"Extracted {len(top_artist_ids)} top artist IDs by frequency")
        
        # Pass these IDs specifically to the engine
        user_features_data['custom_seeds'] = {'artist_ids': top_artist_ids}
        
        # Validate: Check if we have ANY seeds
        top_genres = user_features_data.get('features', {}).get('genre', {}).get('top_genres', [])
        
        if not top_artist_ids and not top_genres:
            raise HTTPException(
                status_code=400,
                detail="Not enough data to generate recommendations. Please listen to more music on Spotify and try again!"
            )
        
        # Generate!
        recs = engine.generate_recommendations(
            user_features=user_features_data,
            cluster_label=cluster_label,
            limit=limit
        )
        
        # Add explanations (Day 10 enhancement)
        from ml.explainability import add_explanations_to_recommendations
        if 'tracks' in recs and recs['tracks']:
            recs['tracks'] = add_explanations_to_recommendations(recs['tracks'], cluster_label)
        
        return recs


    except Exception as e:
        from fastapi import HTTPException
        import traceback
        print(f"Error generating recommendations: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluation")
def get_model_evaluation(
    token_data: dict = Depends(get_current_user_token)
):
    """
    Get model evaluation metrics (Precision@K, Recall@K, F1@K, etc.)
    
    This demonstrates analytical rigor - critical for Ivy League applications!
    """
    try:
        user_id = token_data['user_id']
        
        # 1. Load user features
        if not storage.features_exist(user_id):
            raise HTTPException(status_code=404, detail="User features not found - please Compute Features first")
            
        user_features_data = storage.load_features(user_id)
        
        # 2. Get user's actual track IDs (ground truth)
        user_track_ids = user_features_data['features'].get('track_ids', [])
        
        # 3. Get cluster
        from ml.clustering import clusterer
        cluster_id, cluster_label = clusterer.predict_cluster(user_features_data['features'])
        
        # 4. Generate recommendations
        # We need raw user data for artist seeds (features only has stats)
        if not storage.data_exists(user_id):
             raise HTTPException(status_code=404, detail="User data not found")
        
        user_data = storage.load_user_data(user_id)
        
        from ml.recommendations import RecommendationEngineV2
        sp_client = SpotifyDataClient(token_data['spotify_access_token'])
        engine = RecommendationEngineV2(sp_client)
        
        # Extract artist IDs from raw profile data
        from collections import Counter
        artist_counts = Counter()
        
        # Use medium term tracks for seeds
        if 'top_tracks_medium' in user_data:
            for track in user_data['top_tracks_medium']:
                for artist in track.get('artists', []):
                    artist_id = artist.get('id')
                    if artist_id and len(artist_id) == 22:
                        artist_counts[artist_id] += 1
                        
        top_artist_ids = [artist_id for artist_id, count in artist_counts.most_common(10)]
        
        # Add seeds to features for the engine
        user_features_data['features']['custom_seeds'] = {'artist_ids': top_artist_ids}
        
        recs = engine.generate_recommendations(
            user_features=user_features_data['features'],
            cluster_label=cluster_label,
            limit=20
        )
        
        # 5. Evaluate recommendations
        from ml.evaluation import evaluate_recommendations
        
        # Get user genres from features
        user_genres = set(user_features_data['features'].get('genre_distribution', {}).keys())
        
        if 'tracks' in recs and recs['tracks']:
            metrics = evaluate_recommendations(
                recs['tracks'],
                user_genres,
                k=10
            )
        else:
            metrics = {
                'precision_at_k': 0.0,
                'recall_at_k': 0.0,
                'f1_at_k': 0.0,
                'diversity_score': 0.0,
                'novelty_score': 0.0,
                'k': 10
            }
        
        # 6. Return evaluation results
        return {
            'metrics': metrics,
            'cluster': cluster_label,
            'total_user_tracks': len(user_track_ids),
            'total_recommendations': len(recs.get('tracks', []))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        from fastapi import HTTPException
        import traceback
        print(f"Error generating evaluation: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights")
def get_user_insights(token_data: dict = Depends(get_current_user_token)):
    """
    Get advanced ML insights (Day 12):
    - Cluster Comparison
    - Taste Evolution
    - Entropy (Diversity) Score
    """
    try:
        user_id = token_data['user_id']
        
        # 1. Load Data
        if not storage.features_exist(user_id) or not storage.data_exists(user_id):
             raise HTTPException(status_code=404, detail="User data missing. Please refresh profile.")
             
        user_features_data = storage.load_features(user_id)
        user_data = storage.load_user_data(user_id)
        
        features = user_features_data['features']
        
        from ml.insights import (
            calculate_shannon_entropy,
            analyze_genre_evolution,
            calculate_cluster_deviation,
            calculate_genre_distribution_from_tracks,
            calculate_mood_profile,
            CLUSTER_BASELINES
        )
        
        # 2. Calculate Entropy (Diversity) from fresh data
        # Create artist map for fast lookup
        artist_map = {a['id']: a for a in user_data.get('artists', [])}
        
        # Get all tracks (medium term for overall taste)
        all_tracks = user_data.get('top_tracks_medium', [])
        all_genres_dist = calculate_genre_distribution_from_tracks(all_tracks, artist_map)
        entropy_score = calculate_shannon_entropy(all_genres_dist)
        
        # 3. Calculate Mood Profile
        mood_profile = calculate_mood_profile(features)
        
        # 4. Calculate Cluster Deviation
        from ml.clustering import clusterer
        cluster_id, cluster_label = clusterer.predict_cluster(features)
        cluster_baseline = CLUSTER_BASELINES.get(cluster_label, {})
        deviation_data = calculate_cluster_deviation(features, cluster_baseline)
        
        # 5. Calculate Evolution (Short vs Long Term)
        
        short_term_tracks = user_data.get('top_tracks_short', [])
        long_term_tracks = user_data.get('top_tracks_long', [])
        
        st_genres = calculate_genre_distribution_from_tracks(short_term_tracks, artist_map)
        lt_genres = calculate_genre_distribution_from_tracks(long_term_tracks, artist_map)
        
        evolution_data = analyze_genre_evolution(st_genres, lt_genres)
        
        return {
            "cluster_label": cluster_label,
            "entropy_score": round(entropy_score, 3), # 0-4 typical range
            "mood": mood_profile,
            "deviation": deviation_data,
            "evolution": evolution_data
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating insights: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations/content")
def get_content_based_recommendations(
    token_data: dict = Depends(get_current_user_token),
    limit: int = 20
):
    """
    Get content-based recommendations using genre similarity
    
    This endpoint uses genre-based content filtering to recommend tracks
    that match the user's genre preferences.
    """
    try:
        user_id = token_data['user_id']
        
        # 1. Load user features
        user_features_data = load_features(user_id)
        if not user_features_data:
            raise HTTPException(status_code=404, detail="User features not found. Please compute features first.")
        
        # 2. Initialize content-based recommender
        from ml.content_based import ContentBasedRecommender
        sp_client = SpotifyDataClient(token_data['spotify_access_token'])
        recommender = ContentBasedRecommender(sp_client)
        
        # 3. Get recommendations
        print(f"Generating content-based recommendations for user {user_id}")
        recommendations = recommender.get_recommendations(
            user_features_data['features'],
            limit=limit
        )
        
        # 4. Check for errors
        if 'error' in recommendations:
            raise HTTPException(status_code=400, detail=recommendations['error'])
        
        # 5. Add explanations
        from ml.explainability import RecommendationExplainer
        from ml.clustering import clusterer
        
        # Get user's cluster
        cluster_id, cluster_label = clusterer.predict_cluster(user_features_data['features'])
        
        explainer = RecommendationExplainer(sp_client)
        if 'tracks' in recommendations and recommendations['tracks']:
            explained_tracks = explainer.explain_recommendations(
                recommendations['tracks'],
                user_features_data['features'],
                cluster_label
            )
            recommendations['tracks'] = explained_tracks
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating content-based recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluation")
def get_model_evaluation(
    token_data: dict = Depends(get_current_user_token)
):
    """
    Get model evaluation metrics and algorithm comparison
    
    This endpoint demonstrates analytical rigor by comparing:
    - Pure artist-based recommendations
    - Pure genre-based recommendations  
    - Hybrid approach (Resona)
    
    Returns Precision@K, Recall@K, diversity metrics, etc.
    """
    try:
        user_id = token_data['user_id']
        
        # 1. Load user features
        user_features_data = load_features(user_id)
        if not user_features_data:
            raise HTTPException(status_code=404, detail="User features not found")
        
        # 2. Get cluster
        from ml.clustering import clusterer
        cluster_id, cluster_label = clusterer.predict_cluster(user_features_data['features'])
        
        # 3. Initialize evaluator
        from ml.evaluation import RecommendationEvaluator
        sp_client = SpotifyDataClient(token_data['spotify_access_token'])
        evaluator = RecommendationEvaluator(sp_client)
        
        # 4. Compare algorithms
        print(f"Evaluating recommendation algorithms for user {user_id}")
        comparison = evaluator.compare_algorithms(
            user_features_data['features'],
            cluster_label,
            limit=10
        )
        
        # 5. Get hybrid recommendations and evaluate
        from ml.recommendations_v2 import RecommendationEngineV2
        engine = RecommendationEngineV2(sp_client)
        
        # Extract artist IDs
        from collections import Counter
        artist_counts = Counter()
        if 'top_tracks_medium' in user_features_data.get('features', {}).get('raw_data', {}):
            for track in user_features_data['features']['raw_data']['top_tracks_medium']:
                for artist in track.get('artists', []):
                    artist_id = artist.get('id')
                    if artist_id and len(artist_id) == 22:
                        artist_counts[artist_id] += 1
        
        top_artist_ids = [artist_id for artist_id, count in artist_counts.most_common(10)]
        user_features_data['features']['custom_seeds'] = {'artist_ids': top_artist_ids}
        
        hybrid_recs = engine.generate_recommendations(
            user_features=user_features_data['features'],
            cluster_label=cluster_label,
            limit=10,
            diversity=0.5,
            use_genre_boost=True
        )
        
        # Evaluate hybrid
        if 'tracks' in hybrid_recs and hybrid_recs['tracks']:
            hybrid_metrics = evaluator.evaluate_recommendations(
                hybrid_recs['tracks'],
                user_features_data['features'],
                k=10
            )
            comparison['hybrid']['metrics'] = hybrid_metrics
            comparison['hybrid']['tracks'] = hybrid_recs['tracks'][:3]  # Sample
        
        # 6. Generate report
        report = evaluator.generate_evaluation_report(comparison)
        
        # 7. Add comparison data
        report['comparison'] = {
            'artist_based': comparison['artist_based']['metrics'],
            'genre_based': comparison['genre_based']['metrics'],
            'hybrid': comparison['hybrid']['metrics']
        }
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

