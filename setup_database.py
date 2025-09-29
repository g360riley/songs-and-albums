#!/usr/bin/env python3

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

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
            print("Created favorite_songs table")

            cursor.execute("SELECT COUNT(*) as count FROM favorite_songs")
            result = cursor.fetchone()

            if result['count'] == 0:
                # Gage's favorite songs from SoundCloud
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
                    ('Neon Rush', 'Gage Riley', 'Unknown', 'Electronic/Original', 2024, 5, 'My own electronic creation'),
                    ('Twerk it Like Miley', 'Gage Riley', 'Unknown', 'Electronic/Fun', 2022, 4, 'Playful electronic track'),
                    ('Hardbass XP', 'Gage Riley', 'Unknown', 'Hardbass', 2020, 4, 'My hardbass experiment')
                ]

                cursor.executemany('''
                INSERT INTO favorite_songs (song_title, artist, album, genre, release_year, rating, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', favorite_songs)
                print("Added Gage's favorite songs from SoundCloud")
            else:
                print(f"Table already contains {result['count']} songs")

            connection.commit()
            print("Database setup completed successfully!")

    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_favorite_songs_table()