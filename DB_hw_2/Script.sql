CREATE TABLE IF NOT EXISTS Genre (
    id SERIAL PRIMARY KEY,
    genre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Artists (
    id SERIAL PRIMARY KEY,
    artist VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genre_Artist (
    id SERIAL PRIMARY KEY,
    genre_id INTEGER NOT NULL REFERENCES Genre(id),
    artist_id INTEGER NOT NULL REFERENCES Artists(id),
    UNIQUE (genre_id, artist_id)
);

CREATE TABLE IF NOT EXISTS Album (
    id SERIAL PRIMARY KEY,
    release_year SMALLINT NOT NULL,
    album VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Artist_Album (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER NOT NULL REFERENCES Artists(id),
    album_id INTEGER NOT NULL REFERENCES Album(id),
    UNIQUE (artist_id, album_id)
);

CREATE TABLE IF NOT EXISTS Track (
    id SERIAL PRIMARY KEY,
    album_id INTEGER NOT NULL REFERENCES Album(id),
    duration INTERVAL NOT NULL,
    track VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Collection (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    release_year SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Track_Collection (
    id SERIAL PRIMARY KEY,
    track_id INTEGER NOT NULL REFERENCES Track(id),
    collection_id INTEGER NOT NULL REFERENCES Collection(id),
    UNIQUE (track_id, collection_id)
);
