from typing import Optional
import yt_dlp

from song_model import Song
from song_dao import (
    dao_get_songs_missing_youtube_url,
    dao_get_pending_download_songs,
    dao_update_song,
)
from Youtube.downloader import download_song_audio


def build_youtube_query(song: Song) -> str:
    return f"{song.title} {song.artist} official audio"


def search_youtube_for_song(song: Song) -> Optional[str]:
    query = build_youtube_query(song)

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch1:{query}", download=False)

        if not result:
            return None

        entries = result.get("entries", [])
        if not entries:
            return None

        first = entries[0]
        return first.get("webpage_url")

    except Exception as e:
        print(f"YouTube search failed for '{song.title}' by '{song.artist}': {e}")
        return None


def resolve_youtube_urls_for_all_pending_songs() -> None:
    songs = dao_get_songs_missing_youtube_url()

    if not songs:
        print("No songs are waiting for YouTube matching.")
        return

    print(f"Found {len(songs)} song(s) needing YouTube URLs.")

    resolved_count = 0
    failed_count = 0

    for index, song in enumerate(songs, start=1):
        print(f"[{index}/{len(songs)}] Searching: {song.title} - {song.artist}")

        youtube_url = search_youtube_for_song(song)

        if youtube_url:
            song.youtube_url = youtube_url
            dao_update_song(song)
            resolved_count += 1
            print(f"Matched: {youtube_url}")
        else:
            failed_count += 1
            print("No YouTube result found.")

    print("\nYouTube resolution completed.")
    print(f"Resolved: {resolved_count}")
    print(f"Failed: {failed_count}")


def download_all_pending_songs(audio_format: str = "mp3") -> None:
    songs = dao_get_pending_download_songs()

    if not songs:
        print("No songs are waiting to be downloaded.")
        return

    print(f"Found {len(songs)} song(s) ready for download.")

    downloaded_count = 0
    failed_count = 0

    for index, song in enumerate(songs, start=1):
        print(f"[{index}/{len(songs)}] Downloading: {song.title} - {song.artist}")

        file_path = download_song_audio(song, output_dir="downloads", audio_format=audio_format)

        if file_path:
            song.downloaded = True
            song.file_path = file_path
            dao_update_song(song)
            downloaded_count += 1
            print(f"Saved: {file_path}")
        else:
            failed_count += 1
            print("Download failed.")

    print("\nDownload process completed.")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")