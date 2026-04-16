from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'EswarNiran',  # your MySQL password
    'database': 'mus_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ✅ Artists API
@app.route('/artists', methods=['GET'])
def get_artists():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    offset = (page - 1) * limit
    search = request.args.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        like_pattern = f"%{search}%"
        cursor.execute("SELECT COUNT(*) as total FROM artists WHERE name LIKE %s", (like_pattern,))
        total = cursor.fetchone()['total']

        cursor.execute("""
            SELECT id, name, followers, genres, popularity
            FROM artists
            WHERE name LIKE %s
            LIMIT %s OFFSET %s
        """, (like_pattern, limit, offset))
    else:
        cursor.execute("SELECT COUNT(*) as total FROM artists")
        total = cursor.fetchone()['total']

        cursor.execute("""
            SELECT id, name, followers, genres, popularity
            FROM artists
            LIMIT %s OFFSET %s
        """, (limit, offset))

    artists = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({
        'page': page,
        'limit': limit,
        'total': total,
        'artists': artists
    })

# ✅ Tracks API
@app.route('/tracks', methods=['GET'])
def get_tracks():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    offset = (page - 1) * limit
    search = request.args.get('search', '')
    min_popularity = int(request.args.get('min_popularity', 0))
    max_popularity = int(request.args.get('max_popularity', 100))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    count_query = "SELECT COUNT(*) as total FROM tracks WHERE popularity BETWEEN %s AND %s"
    params = [min_popularity, max_popularity]

    if search:
        count_query += " AND name LIKE %s"
        params.append(f"%{search}%")

    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']

    select_query = count_query.replace("COUNT(*) as total", "*") + " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(select_query, params)
    tracks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        'page': page,
        'limit': limit,
        'total': total,
        'tracks': tracks
    })

# ✅ Dashboard SQL Endpoints
@app.route('/sql/top-artists')
def top_artists():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, popularity FROM artists ORDER BY popularity DESC LIMIT 10;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/sql/top-tracks')
def top_tracks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, popularity FROM tracks ORDER BY popularity DESC LIMIT 10;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/sql/tracks-per-year')
def tracks_per_year():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT YEAR(release_date) AS release_year, ROUND(AVG(popularity), 2) AS avg_popularity
        FROM tracks WHERE release_date IS NOT NULL
        GROUP BY release_year ORDER BY release_year DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/sql/top-genres')
def top_genres():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT genres, AVG(popularity) AS avg_popularity
        FROM artists
        WHERE genres <> ''
        GROUP BY genres
        ORDER BY avg_popularity DESC
        LIMIT 10;
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/')
def home():
    return {"message": "Welcome to the MelodyMatrix Music API"}

if __name__ == '__main__':
    app.run(debug=True)
