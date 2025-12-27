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
