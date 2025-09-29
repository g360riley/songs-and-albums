from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

favorite_songs = Blueprint('favorite_songs', __name__)

@favorite_songs.route('/', methods=['GET', 'POST'])
def show_favorite_songs():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        song_title = request.form['song_title']
        artist = request.form['artist']
        album = request.form.get('album', '')
        genre = request.form.get('genre', '')
        release_year = request.form.get('release_year')
        rating = request.form['rating']
        notes = request.form.get('notes', '')

        release_year = int(release_year) if release_year else None

        cursor.execute('''INSERT INTO favorite_songs
                         (song_title, artist, album, genre, release_year, rating, notes)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (song_title, artist, album, genre, release_year, rating, notes))
        db.commit()

        flash('New favorite song added successfully!', 'success')
        return redirect(url_for('favorite_songs.show_favorite_songs'))

    cursor.execute('SELECT * FROM favorite_songs ORDER BY created_at DESC')
    all_songs = cursor.fetchall()
    return render_template('favorite_songs.html', all_songs=all_songs)

@favorite_songs.route('/update_song/<int:song_id>', methods=['POST'])
def update_song(song_id):
    db = get_db()
    cursor = db.cursor()

    song_title = request.form['song_title']
    artist = request.form['artist']
    album = request.form.get('album', '')
    genre = request.form.get('genre', '')
    release_year = request.form.get('release_year')
    rating = request.form['rating']
    notes = request.form.get('notes', '')

    release_year = int(release_year) if release_year else None

    cursor.execute('''UPDATE favorite_songs
                     SET song_title = %s, artist = %s, album = %s, genre = %s,
                         release_year = %s, rating = %s, notes = %s
                     WHERE song_id = %s''',
                   (song_title, artist, album, genre, release_year, rating, notes, song_id))
    db.commit()

    flash('Song updated successfully!', 'success')
    return redirect(url_for('favorite_songs.show_favorite_songs'))

@favorite_songs.route('/delete_song/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM favorite_songs WHERE song_id = %s', (song_id,))
    db.commit()

    flash('Song deleted successfully!', 'danger')
    return redirect(url_for('favorite_songs.show_favorite_songs'))