# Resona Backend

Backend API for Resona - User-Centric Music Recommendation via Behavioral Modeling

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Get Spotify credentials:
   - Go to https://developer.spotify.com/dashboard
   - Create a new app
   - Copy Client ID and Client Secret
   - Add to `.env` file

3. Update `.env` with your credentials

### 5. Test Spotify API Connection

```bash
python test_spotify.py
```

You should see: Spotify API Connection Successful!

### 6. Run the Server

```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app.py                 # Main FastAPI application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── test_spotify.py        # Spotify API test script
├── .env                   # Environment variables (not in git)
├── .env.example           # Environment variables template
│
├── auth/                  # Authentication (OAuth, JWT)
├── data/                  # Cached data (git-ignored)
├── features/              # Feature engineering
├── models/                # ML models
├── services/              # Business logic
└── storage/               # Data storage layer
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Linting
```bash
pylint *.py
```

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn
- **Spotify API**: Spotipy 2.23.0
- **ML**: scikit-learn 1.4.0, NumPy, Pandas
- **Auth**: python-jose (JWT)
