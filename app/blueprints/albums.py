from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db

albums = Blueprint('albums', __name__)

@albums.route('/')
def show_albums():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
    SELECT a.*,
           COUNT(s.song_id) as song_count,
           AVG(s.rating) as avg_rating
    FROM albums a
    LEFT JOIN songs s ON a.album_id = s.album_id
    GROUP BY a.album_id
    ORDER BY a.created_at DESC
    ''')
    all_albums = cursor.fetchall()
    return render_template('albums.html', all_albums=all_albums)

@albums.route('/album/<int:album_id>')
def show_album_details(album_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM albums WHERE album_id = %s', (album_id,))
    album = cursor.fetchone()

    if not album:
        flash('Album not found!', 'error')
        return redirect(url_for('albums.show_albums'))

    cursor.execute('''
    SELECT * FROM songs
    WHERE album_id = %s
    ORDER BY track_number ASC, song_title ASC
    ''', (album_id,))
    songs = cursor.fetchall()

    return render_template('album_details.html', album=album, songs=songs)

@albums.route('/add_album', methods=['POST'])
def add_album():
    db = get_db()
    cursor = db.cursor()

    album_title = request.form['album_title']
    artist = request.form['artist']
    release_year = request.form.get('release_year')
    genre = request.form.get('genre', '')
    album_art_url = request.form.get('album_art_url', '')
    total_tracks = request.form.get('total_tracks')
    notes = request.form.get('notes', '')

    release_year = int(release_year) if release_year else None
    total_tracks = int(total_tracks) if total_tracks else None

    try:
        cursor.execute('''
        INSERT INTO albums (album_title, artist, release_year, genre, album_art_url, total_tracks, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (album_title, artist, release_year, genre, album_art_url, total_tracks, notes))
        db.commit()
        flash('Album added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding album: {str(e)}', 'error')

    return redirect(url_for('albums.show_albums'))

@albums.route('/update_album/<int:album_id>', methods=['POST'])
def update_album(album_id):
    db = get_db()
    cursor = db.cursor()

    album_title = request.form['album_title']
    artist = request.form['artist']
    release_year = request.form.get('release_year')
    genre = request.form.get('genre', '')
    album_art_url = request.form.get('album_art_url', '')
    total_tracks = request.form.get('total_tracks')
    notes = request.form.get('notes', '')

    release_year = int(release_year) if release_year else None
    total_tracks = int(total_tracks) if total_tracks else None

    cursor.execute('''
    UPDATE albums
    SET album_title = %s, artist = %s, release_year = %s, genre = %s,
        album_art_url = %s, total_tracks = %s, notes = %s
    WHERE album_id = %s
    ''', (album_title, artist, release_year, genre, album_art_url, total_tracks, notes, album_id))
    db.commit()

    flash('Album updated successfully!', 'success')
    return redirect(url_for('albums.show_albums'))

@albums.route('/delete_album/<int:album_id>', methods=['POST'])
def delete_album(album_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM albums WHERE album_id = %s', (album_id,))
    db.commit()

    flash('Album deleted successfully!', 'danger')
    return redirect(url_for('albums.show_albums'))

@albums.route('/api/albums', methods=['GET'])
def get_albums_api():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
    SELECT album_id, album_title, artist
    FROM albums
    ORDER BY album_title ASC
    ''')
    albums_list = cursor.fetchall()
    return jsonify(albums_list)