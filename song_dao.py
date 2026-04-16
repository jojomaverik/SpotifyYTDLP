from typing import List
from sqlmodel import Session, select, delete
from song_model import Song
from db import engine


def dao_get_all_songs() -> List[Song]:
    with Session(engine) as session:
        statement = select(Song)
        songs = session.exec(statement).all()
        return list(songs)

def dao_save_song(songs: List[Song]):
    with Session(engine) as session:
        session.add_all(songs)
        session.commit()

def dao_clear_songs() -> None:
    with Session(engine) as session:
        session.exec(delete(Song))
        session.commit()

def dao_get_song_by_spotify_id(spotify_id: str) -> Optional[Song]:
    with Session(engine) as session:
        statement = select(Song).where(Song.spotify_id == spotify_id)
        return session.exec(statement).first()


def dao_get_songs_missing_youtube_url() -> List[Song]:
    with Session(engine) as session:
        statement = select(Song).where(Song.youtube_url == None)  # noqa: E711
        songs = session.exec(statement).all()
        return list(songs)


def dao_get_pending_download_songs() -> List[Song]:
    with Session(engine) as session:
        statement = select(Song).where(
            Song.youtube_url != None,   # noqa: E711
            Song.downloaded == False
        )
        songs = session.exec(statement).all()
        return list(songs)
