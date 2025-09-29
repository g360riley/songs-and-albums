-- Create table for favorite songs
CREATE TABLE favorite_songs (
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
);

-- Insert some sample data
INSERT INTO favorite_songs (song_title, artist, album, genre, release_year, rating, notes) VALUES
('Bohemian Rhapsody', 'Queen', 'A Night at the Opera', 'Rock', 1975, 5, 'A masterpiece of progressive rock'),
('Billie Jean', 'Michael Jackson', 'Thriller', 'Pop', 1982, 5, 'Iconic pop song with amazing beat'),
('Hotel California', 'Eagles', 'Hotel California', 'Rock', 1976, 4, 'Classic rock anthem'),
('Imagine', 'John Lennon', 'Imagine', 'Pop', 1971, 5, 'Beautiful and peaceful message'),
('Sweet Child O'' Mine', 'Guns N'' Roses', 'Appetite for Destruction', 'Hard Rock', 1987, 4, 'Great guitar work');