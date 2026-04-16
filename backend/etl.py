import pandas as pd
import mysql.connector
from datetime import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Your_password',
    'database': 'mus_db'
}

def transform_date(date_str):
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue
    return None

def load_artists(csv_path, cursor, batch_size=1000):
    print(f"Reading artists CSV from: {csv_path}")
    df = pd.read_csv(csv_path)
    df.fillna({'followers':0, 'genres':'', 'popularity':0, 'name':'', 'id':''}, inplace=True)

    data = []
    for i, row in df.iterrows():
        data.append((
            row['id'], int(row['followers']), row['genres'], row['name'], int(row['popularity'])
        ))
        if len(data) >= batch_size:
            try:
                cursor.executemany("""
                    INSERT INTO artists (id, followers, genres, name, popularity)
                    VALUES (%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE 
                        followers=VALUES(followers),
                        genres=VALUES(genres),
                        name=VALUES(name),
                        popularity=VALUES(popularity)
                """, data)
                print(f"Inserted/Updated {i+1} artists")
            except Exception as e:
                print(f"Error at artist batch ending {i}: {e}")
            data.clear()

    if data:
        try:
            cursor.executemany("""
                INSERT INTO artists (id, followers, genres, name, popularity)
                VALUES (%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    followers=VALUES(followers),
                    genres=VALUES(genres),
                    name=VALUES(name),
                    popularity=VALUES(popularity)
            """, data)
            print(f"Inserted/Updated all {len(df)} artists")
        except Exception as e:
            print(f"Error in final artist batch: {e}")

def load_tracks(csv_path, cursor, batch_size=1000):
    print(f"Reading tracks CSV from: {csv_path}")
    df = pd.read_csv(csv_path)
    df.fillna({'popularity':0, 'duration_ms':0, 'explicit':False, 'artists':'', 'id_artists':'',
               'release_date':'', 'danceability':0, 'energy':0, 'key':0, 'loudness':0, 'mode':0,
               'speechiness':0, 'acousticness':0, 'instrumentalness':0, 'liveness':0, 'valence':0,
               'tempo':0, 'time_signature':0, 'name':''}, inplace=True)

    data = []
    for i, row in df.iterrows():
        release_date = transform_date(row['release_date']) if row['release_date'] else None
        explicit = str(row['explicit']).lower() in ['1','true','yes']

        data.append((
            row['id'],
            row['name'][:255],  # truncate name to 255 chars for VARCHAR
            int(row['popularity']),
            int(row['duration_ms']),
            explicit,
            row['artists'],
            row['id_artists'],
            release_date,
            float(row['danceability']),
            float(row['energy']),
            int(row['key']),
            float(row['loudness']),
            int(row['mode']),
            float(row['speechiness']),
            float(row['acousticness']),
            float(row['instrumentalness']),
            float(row['liveness']),
            float(row['valence']),
            float(row['tempo']),
            int(row['time_signature'])
        ))

        if len(data) >= batch_size:
            try:
                cursor.executemany("""
                    INSERT INTO tracks (
                        id, name, popularity, duration_ms, explicit, artists, id_artists, release_date,
                        danceability, energy, `key`, loudness, mode, speechiness, acousticness,
                        instrumentalness, liveness, valence, tempo, time_signature
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                        name=VALUES(name),
                        popularity=VALUES(popularity),
                        duration_ms=VALUES(duration_ms),
                        explicit=VALUES(explicit),
                        artists=VALUES(artists),
                        id_artists=VALUES(id_artists),
                        release_date=VALUES(release_date),
                        danceability=VALUES(danceability),
                        energy=VALUES(energy),
                        `key`=VALUES(`key`),
                        loudness=VALUES(loudness),
                        mode=VALUES(mode),
                        speechiness=VALUES(speechiness),
                        acousticness=VALUES(acousticness),
                        instrumentalness=VALUES(instrumentalness),
                        liveness=VALUES(liveness),
                        valence=VALUES(valence),
                        tempo=VALUES(tempo),
                        time_signature=VALUES(time_signature)
                """, data)
                print(f"Inserted/Updated {i+1} tracks")
            except Exception as e:
                print(f"Error at track batch ending {i}: {e}")
            data.clear()

    if data:
        try:
            cursor.executemany("""
                INSERT INTO tracks (
                    id, name, popularity, duration_ms, explicit, artists, id_artists, release_date,
                    danceability, energy, `key`, loudness, mode, speechiness, acousticness,
                    instrumentalness, liveness, valence, tempo, time_signature
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    name=VALUES(name),
                    popularity=VALUES(popularity),
                    duration_ms=VALUES(duration_ms),
                    explicit=VALUES(explicit),
                    artists=VALUES(artists),
                    id_artists=VALUES(id_artists),
                    release_date=VALUES(release_date),
                    danceability=VALUES(danceability),
                    energy=VALUES(energy),
                    `key`=VALUES(`key`),
                    loudness=VALUES(loudness),
                    mode=VALUES(mode),
                    speechiness=VALUES(speechiness),
                    acousticness=VALUES(acousticness),
                    instrumentalness=VALUES(instrumentalness),
                    liveness=VALUES(liveness),
                    valence=VALUES(valence),
                    tempo=VALUES(tempo),
                    time_signature=VALUES(time_signature)
            """, data)
            print(f"Inserted/Updated all {len(df)} tracks")
        except Exception as e:
            print(f"Error in final track batch: {e}")

def main():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to MySQL database")

        load_artists(r"D:\my_project\backend\data\artists.csv", cursor)
        load_tracks(r"D:\my_project\backend\data\tracks.csv", cursor)

        conn.commit()
        cursor.close()
        conn.close()
        print("ETL process completed successfully")
    except Exception as e:
        print(f"Fatal error during ETL: {e}")

if __name__ == "__main__":
    main()
