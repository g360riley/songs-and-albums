#!/usr/bin/env python3

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_albums_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS albums (
        album_id INT AUTO_INCREMENT PRIMARY KEY,
        album_title VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL,
        release_year INT,
        genre VARCHAR(100),
        album_art_url VARCHAR(500),
        total_tracks INT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY unique_album_artist (album_title, artist)
    )
    ''')
    print("Created albums table")

def create_songs_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        song_id INT AUTO_INCREMENT PRIMARY KEY,
        song_title VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL,
        album_id INT,
        track_number INT,
        duration_seconds INT,
        genre VARCHAR(100),
        rating INT CHECK (rating >= 1 AND rating <= 5),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE SET NULL,
        INDEX idx_album_id (album_id),
        INDEX idx_artist (artist),
        INDEX idx_rating (rating)
    )
    ''')
    print("Created songs table")

def create_favorite_songs_table():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            create_albums_table(cursor)
            create_songs_table(cursor)

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorite_songs (
                song_id INT AUTO_INCREMENT PRIMARY KEY,
                song_title VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                album VARCHAR(255),
                genre VARCHAR(100),
                release_year INT,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            ''')
            print("Created favorite_songs table (legacy)")

            # Add sample albums
            cursor.execute("SELECT COUNT(*) as count FROM albums")
            result = cursor.fetchone()

            if result['count'] == 0:
                sample_albums = [
                    ('Skin', 'Flume', 2016, 'Electronic/Alternative', None, 16, 'Acclaimed electronic album'),
                    ('Gage Riley Singles', 'Gage Riley', 2024, 'Electronic/Original', None, 3, 'Collection of original tracks'),
                    ('Unknown Singles', 'Various Artists', None, 'Mixed', None, None, 'Collection of singles without album info')
                ]

                cursor.executemany('''
                INSERT INTO albums (album_title, artist, release_year, genre, album_art_url, total_tracks, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', sample_albums)
                print("Added sample albums")

            # Get album IDs for referencing
            cursor.execute("SELECT album_id, album_title, artist FROM albums")
            albums = cursor.fetchall()
            album_lookup = {(album['album_title'], album['artist']): album['album_id'] for album in albums}

            # Add sample songs with proper album relationships
            cursor.execute("SELECT COUNT(*) as count FROM songs")
            result = cursor.fetchone()

            if result['count'] == 0:
                songs_data = [
                    ('Like A Prayer', 'GALWARO', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Electronic/Dance', 5, 'Remix of classic Madonna track'),
                    ('DISARM YOU (WUB FLIP)', 'WUB', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Dubstep/Bass', 5, 'Heavy bass flip'),
                    ('Tattoo (Topic Remix)', 'Loreen', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Electronic/Pop', 4, 'Eurovision winner remix'),
                    ('Just Hold On', 'Steve Aoki & Louis Tomlinson', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'EDM/Pop', 4, 'Collaboration between EDM and pop'),
                    ('Piercing Light (The Siberian Hardstyle Edit)', 'The Siberian', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Hardstyle', 5, 'Hardstyle edit of League of Legends track'),
                    ('Memories (feat. Kid Cudi) [2021 Remix]', 'David Guetta', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'EDM/Hip-Hop', 4, 'Guetta and Cudi collaboration'),
                    ('Weekend', 'Louis The Child', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Future Bass', 4, 'Chill future bass vibes'),
                    ('Say It', 'Flume ft. Tove Lo', album_lookup.get(('Skin', 'Flume')), 3, 240, 'Electronic/Alternative', 5, 'Beautiful electronic production'),
                    ('Alive', 'Ghost in Real Life', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Electronic', 4, 'Modern electronic track'),
                    ('LEAVEMEALONE (CRANKDAT REMIX)', 'Crankdat', album_lookup.get(('Unknown Singles', 'Various Artists')), None, None, 'Dubstep/Trap', 5, 'High-energy remix'),
                    ('Neon Rush', 'Gage Riley', album_lookup.get(('Gage Riley Singles', 'Gage Riley')), 1, 180, 'Electronic/Original', 5, 'My own electronic creation'),
                    ('Twerk it Like Miley', 'Gage Riley', album_lookup.get(('Gage Riley Singles', 'Gage Riley')), 2, 165, 'Electronic/Fun', 4, 'Playful electronic track'),
                    ('Hardbass XP', 'Gage Riley', album_lookup.get(('Gage Riley Singles', 'Gage Riley')), 3, 200, 'Hardbass', 4, 'My hardbass experiment')
                ]

                cursor.executemany('''
                INSERT INTO songs (song_title, artist, album_id, track_number, duration_seconds, genre, rating, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', songs_data)
                print("Added songs with album relationships")

            # Keep legacy favorite_songs table for backward compatibility
            cursor.execute("SELECT COUNT(*) as count FROM favorite_songs")
            result = cursor.fetchone()

            if result['count'] == 0:
                # Gage's favorite songs from SoundCloud (legacy format)
                favorite_songs = [
                    ('Like A Prayer', 'GALWARO', 'Unknown', 'Electronic/Dance', 2020, 5, 'Remix of classic Madonna track'),
                    ('DISARM YOU (WUB FLIP)', 'WUB', 'Unknown', 'Dubstep/Bass', 2025, 5, 'Heavy bass flip'),
                    ('Tattoo (Topic Remix)', 'Loreen', 'Unknown', 'Electronic/Pop', 2023, 4, 'Eurovision winner remix'),
                    ('Just Hold On', 'Steve Aoki & Louis Tomlinson', 'Unknown', 'EDM/Pop', 2016, 4, 'Collaboration between EDM and pop'),
                    ('Piercing Light (The Siberian Hardstyle Edit)', 'The Siberian', 'Unknown', 'Hardstyle', 2020, 5, 'Hardstyle edit of League of Legends track'),
                    ('Memories (feat. Kid Cudi) [2021 Remix]', 'David Guetta', 'Unknown', 'EDM/Hip-Hop', 2020, 4, 'Guetta and Cudi collaboration'),
                    ('Weekend', 'Louis The Child', 'Unknown', 'Future Bass', 2016, 4, 'Chill future bass vibes'),
                    ('Say It', 'Flume ft. Tove Lo', 'Skin', 'Electronic/Alternative', 2016, 5, 'Beautiful electronic production'),
                    ('Alive', 'Ghost in Real Life', 'Unknown', 'Electronic', 2024, 4, 'Modern electronic track'),
                    ('LEAVEMEALONE (CRANKDAT REMIX)', 'Crankdat', 'Unknown', 'Dubstep/Trap', 2024, 5, 'High-energy remix'),
                    ('Neon Rush', 'Gage Riley', 'Gage Riley Singles', 'Electronic/Original', 2024, 5, 'My own electronic creation'),
                    ('Twerk it Like Miley', 'Gage Riley', 'Gage Riley Singles', 'Electronic/Fun', 2022, 4, 'Playful electronic track'),
                    ('Hardbass XP', 'Gage Riley', 'Gage Riley Singles', 'Hardbass', 2020, 4, 'My hardbass experiment')
                ]

                cursor.executemany('''
                INSERT INTO favorite_songs (song_title, artist, album, genre, release_year, rating, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', favorite_songs)
                print("Added Gage's favorite songs from SoundCloud (legacy table)")
            else:
                print(f"Legacy table already contains {result['count']} songs")

            connection.commit()
            print("Database setup completed successfully!")

    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_favorite_songs_table()