#search_youtube(song) -> url
from typing import Optional
import yt_dlp
from song_model import Song


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
            print(f"Search results for '{query}': {result}")  # Debug print

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


# Test block
if __name__ == "__main__":
    test_song = Song(
        title="Numb",
        artist="Linkin Park",
        album="Meteora",
        spotify_id="test"
    )

    url = search_youtube_for_song(test_song)
    print("Found URL:", url)
    
    