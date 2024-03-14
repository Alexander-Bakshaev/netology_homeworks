---Задание 2---

-- 1. Название и продолжительность самого длительного трека
SELECT track, duration
FROM Track
WHERE duration = (
    SELECT MAX(duration)
    FROM Track
);

-- 2. Название треков, продолжительность которых не менее 3,5 минут
SELECT track
FROM Track
WHERE duration >= 210;

-- 3. Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT title
FROM Collection
WHERE release_year BETWEEN 2018 AND 2020;

-- 4. Исполнители, чье имя состоит из одного слова
SELECT artist
FROM Artists
WHERE artist NOT LIKE '% %';

-- 5. Название треков, которые содержат слово «мой» или «my»
SELECT track
FROM Track
WHERE LOWER(track) LIKE '%мой%' OR LOWER(track) LIKE '%my%';


---Задание 3---

-- 1. Количество исполнителей в каждом жанре
SELECT g.genre, COUNT(ga.artist_id) AS num_artists
FROM Genre g
LEFT JOIN Genre_Artist ga ON g.id = ga.genre_id
GROUP BY g.genre;

-- 2. Количество треков, вошедших в альбомы 2019–2020 годов
SELECT COUNT(t.id) AS num_tracks
FROM Track t
INNER JOIN Album a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- 3. Средняя продолжительность треков по каждому альбому
SELECT a.album, AVG(t.duration) AS avg_duration
FROM Album a
INNER JOIN Track t ON a.id = t.album_id
GROUP BY a.album;

-- 4. Все исполнители, которые не выпустили альбомы в 2020 году
SELECT artist
FROM Artists
WHERE id NOT IN (
    SELECT DISTINCT artist_id
    FROM Artist_Album
    WHERE album_id IN (
        SELECT id
        FROM Album
        WHERE release_year = 2020
    )
);

-- 5. Названия сборников, в которых присутствует конкретный исполнитель "Земфира"
SELECT DISTINCT c.title
FROM Collection AS c
JOIN Track_Collection AS tc ON c.id = tc.collection_id
JOIN Track AS t ON tc.track_id = t.id
JOIN Album AS a ON t.album_id = a.id
JOIN Artist_Album AS aa ON a.id = aa.album_id
JOIN Artists AS ar ON aa.artist_id = ar.id
WHERE ar.artist = 'Земфира';



---Задание 4---

-- 1. Названия альбомов, в которых присутствуют исполнители более чем одного жанра
SELECT DISTINCT Album.album
FROM Album
JOIN Artist_Album ON Album.id = Artist_Album.album_id
JOIN Genre_Artist ON Artist_Album.artist_id = Genre_Artist.artist_id
GROUP BY Album.album
HAVING COUNT(DISTINCT Genre_Artist.genre_id) > 1;

-- 2. Наименования треков, которые не входят в сборники
SELECT t.track
FROM Track t
LEFT JOIN Track_Collection tc ON t.id = tc.track_id
WHERE tc.id IS NULL;

-- 3. Исполнитель или исполнители, написавшие самый короткий по продолжительности трек
SELECT ar.artist
FROM Artists ar
INNER JOIN Artist_Album aa ON ar.id = aa.artist_id
INNER JOIN Track t ON aa.album_id = t.album_id
WHERE t.duration = (
    SELECT MIN(duration)
    FROM Track
);

-- 4. Названия альбомов, содержащих наименьшее количество треков
SELECT album
FROM Album
WHERE id IN (
    SELECT album_id
    FROM Track
    GROUP BY album_id
    HAVING COUNT(*) = (
        SELECT MIN(track_count)
        FROM (
            SELECT COUNT(*) as track_count
            FROM Track
            GROUP BY album_id
        ) AS min_track_count
    )
);
