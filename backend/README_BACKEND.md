# Backend - Spotify Data API

## Run Backend
```bash
cd backend
pip install -r requirements.txt
python etl.py  # Load data into database
uvicorn main:app --reload
