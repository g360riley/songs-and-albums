from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

songs = Blueprint('songs', __name__)

@songs.route('/')
def show_songs():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
    SELECT s.*,
           a.album_title,
           a.artist as album_artist
    FROM songs s
    LEFT JOIN albums a ON s.album_id = a.album_id
    ORDER BY s.created_at DESC
    ''')
    all_songs = cursor.fetchall()

    cursor.execute('SELECT album_id, album_title, artist FROM albums ORDER BY album_title ASC')
    albums = cursor.fetchall()

    return render_template('songs.html', all_songs=all_songs, albums=albums)

@songs.route('/add_song', methods=['POST'])
def add_song():
    db = get_db()
    cursor = db.cursor()

    song_title = request.form['song_title']
    artist = request.form['artist']
    album_id = request.form.get('album_id')
    track_number = request.form.get('track_number')
    duration_seconds = request.form.get('duration_seconds')
    genre = request.form.get('genre', '')
    rating = request.form['rating']
    notes = request.form.get('notes', '')

    album_id = int(album_id) if album_id else None
    track_number = int(track_number) if track_number else None
    duration_seconds = int(duration_seconds) if duration_seconds else None

    cursor.execute('''
    INSERT INTO songs (song_title, artist, album_id, track_number, duration_seconds, genre, rating, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (song_title, artist, album_id, track_number, duration_seconds, genre, rating, notes))
    db.commit()

    flash('Song added successfully!', 'success')

    # Check if we should return to album details
    return_to_album = request.form.get('return_to_album')
    if return_to_album:
        return redirect(url_for('albums.show_album_details', album_id=return_to_album))

    return redirect(url_for('songs.show_songs'))

@songs.route('/update_song/<int:song_id>', methods=['POST'])
def update_song(song_id):
    db = get_db()
    cursor = db.cursor()

    song_title = request.form['song_title']
    artist = request.form['artist']
    album_id = request.form.get('album_id')
    track_number = request.form.get('track_number')
    duration_seconds = request.form.get('duration_seconds')
    genre = request.form.get('genre', '')
    rating = request.form['rating']
    notes = request.form.get('notes', '')

    album_id = int(album_id) if album_id else None
    track_number = int(track_number) if track_number else None
    duration_seconds = int(duration_seconds) if duration_seconds else None

    cursor.execute('''
    UPDATE songs
    SET song_title = %s, artist = %s, album_id = %s, track_number = %s,
        duration_seconds = %s, genre = %s, rating = %s, notes = %s
    WHERE song_id = %s
    ''', (song_title, artist, album_id, track_number, duration_seconds, genre, rating, notes, song_id))
    db.commit()

    flash('Song updated successfully!', 'success')

    # Check if we should return to album details
    return_to_album = request.form.get('return_to_album')
    if return_to_album:
        return redirect(url_for('albums.show_album_details', album_id=return_to_album))

    return redirect(url_for('songs.show_songs'))

@songs.route('/delete_song/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM songs WHERE song_id = %s', (song_id,))
    db.commit()

    flash('Song deleted successfully!', 'danger')

    # Check if we should return to album details
    return_to_album = request.form.get('return_to_album')
    if return_to_album:
        return redirect(url_for('albums.show_album_details', album_id=return_to_album))

    return redirect(url_for('songs.show_songs'))

def format_duration(seconds):
    if not seconds:
        return "Unknown"
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"

@songs.app_template_filter('duration')
def duration_filter(seconds):
    return format_duration(seconds)