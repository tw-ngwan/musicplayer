import sqlite3
from settings import database_name


# Gets the music score
def get_music_score(song_name: str) -> int:
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT score 
              FROM music
             WHERE title = ?""",
            (song_name, )
        )
        try:
            score = cur.fetchall()[0][0]
        except IndexError:
            score = 0
    return score


# Changes the score of a piece of music
def change_music_score(song_name: str, score: int):
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE music
               SET score = score + ?
             WHERE title = ?""",
            (score, song_name)
        )


# Gets the average score of a genre
def get_average_score(genre: str) -> int:
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT AVG(score) 
              FROM music 
             WHERE genre = ?
            """, (genre, )
        )
        average = cur.fetchall()[0][0]
    return average
