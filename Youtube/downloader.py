import os
import re
from typing import Optional

import yt_dlp

from song_model import Song


def sanitize_filename(value: str) -> str:
    value = re.sub(r'[\\/*?:"<>|]', "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def build_output_template(song: Song, output_dir: str) -> str:
    safe_artist = sanitize_filename(song.artist)
    safe_title = sanitize_filename(song.title)
    filename = f"{safe_artist} - {safe_title}.%(ext)s"
    return os.path.join(output_dir, filename)


def download_song_audio(
    song: Song,
    output_dir: str = "downloads",
    audio_format: str = "mp3"
) -> Optional[str]:
    if not song.youtube_url:
        print(f"Skipping '{song.title}' because no YouTube URL is saved.")
        return None

    os.makedirs(output_dir, exist_ok=True)

    output_template = build_output_template(song, output_dir)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "192" if audio_format == "mp3" else "0",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song.youtube_url])

        final_path = os.path.join(
            output_dir,
            f"{sanitize_filename(song.artist)} - {sanitize_filename(song.title)}.{audio_format}"
        )

        if os.path.exists(final_path):
            return final_path

        print(f"Download finished, but expected file was not found: {final_path}")
        return None

    except Exception as e:
        print(f"Download failed for '{song.title}' by '{song.artist}': {e}")
        return None