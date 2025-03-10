import os
import pandas as pd
from io import StringIO
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")  # e.g., "5433"

def fix_spotify_release_date(date_str):
    """
    Convert Spotify's variable-length date string into a valid YYYY-MM-DD.
    - If '2020' => '2020-01-01'
    - If '2020-05' => '2020-05-01'
    - If '2020-05-25' => '2020-05-25'
    """
    if not date_str:
        return None
    parts = date_str.split('-')
    if len(parts) == 1:
        return date_str + '-01-01'  # e.g. '2011' -> '2011-01-01'
    elif len(parts) == 2:
        return date_str + '-01'     # e.g. '2011-06' -> '2011-06-01'
    else:
        return date_str            # e.g. '2011-06-24' stays the same

def copy_csv_to_db(csv_path, table_name):
    """
    1. Read CSV into a pandas DataFrame.
    2. Fix 'release_date' using fix_spotify_release_date().
    3. COPY the corrected data into PostgreSQL using psycopg2.
    """
    # 1. Read CSV
    df = pd.read_csv(csv_path)
    
    # 2. Fix the release_date column
    if 'release_date' in df.columns:
        df['release_date'] = df['release_date'].apply(fix_spotify_release_date)
    
    # 3. Write DataFrame to an in-memory CSV buffer
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # 4. Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cur = conn.cursor()

    # Optionally set the search path (if your table is in a custom schema):
    cur.execute("SET search_path TO spotify_trends")

    # 5. COPY from the in-memory CSV
    copy_sql = f"""
        COPY {table_name} (
            artist,
            artist_id,
            artist_popularity,
            artist_followers,
            genres,
            track_name,
            track_id,
            track_popularity,
            release_date,
            danceability,
            energy,
            tempo
        )
        FROM STDIN
        WITH CSV
        HEADER
    """
    cur.copy_expert(copy_sql, buffer)

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ CSV data from '{csv_path}' copied into '{table_name}' successfully, with corrected release dates!")

if __name__ == "__main__":
    csv_file_path = "spotify_trending_artists.csv"
    target_table = "music_trends"
    copy_csv_to_db(csv_file_path, target_table)
