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
    
def dao_update_song(updated_song: Song) -> Optional[Song]:
    with Session(engine) as session:
        existing_song = session.get(Song, updated_song.id)

        if not existing_song:
            return None

        existing_song.title = updated_song.title
        existing_song.artist = updated_song.artist
        existing_song.album = updated_song.album
        existing_song.spotify_id = updated_song.spotify_id
        existing_song.youtube_url = updated_song.youtube_url
        existing_song.downloaded = updated_song.downloaded
        existing_song.file_path = updated_song.file_path

        session.add(existing_song)
        session.commit()
        session.refresh(existing_song)
        return existing_song
