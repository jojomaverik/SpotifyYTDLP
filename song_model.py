from typing import Optional
from sqlmodel import Field, SQLModel

class Song(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    album: str
    artist: str
    spotify_id: str

    # Youtube-related fields
    youtube_url: Optional[str] = None
    downloaded: bool = False
    file_path: Optional[str] = None
