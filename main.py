import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from song_model import Song
from song_dao import (
    dao_get_all_songs,
    dao_save_song,
    dao_clear_songs,
    dao_get_songs_missing_youtube_url,
    dao_get_pending_download_songs,
)
from db import create_tables
from spotify_service import get_playlist_tracks
from Youtube.youtube_service import (
    resolve_youtube_urls_for_all_pending_songs,
    download_all_pending_songs,
)


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_songs(query: str) -> List[Song]:
    results: Optional[Dict[str, Any]] = sp.search(query, limit=10)

    if not results or "tracks" not in results:
        return []

    songs: List[Song] = []
    for track in results["tracks"]["items"]:
        song = Song(
            title=track["name"],
            artist=track["artists"][0]["name"],
            album=track["album"]["name"],
            spotify_id=track["id"]
        )
        songs.append(song)

    return songs


if __name__ == "__main__":
    create_tables()

    while True:
        selection = input(
            "\nEnter:\n"
            "s - search songs\n"
            "g - print all songs in the database\n"
            "c - clear database\n"
            "p - import songs from a Spotify playlist URL\n"
            "y - find YouTube URLs for songs in database\n"
            "m - show songs still missing YouTube URLs\n"
            "d - download songs that already have YouTube URLs\n"
            "r - show songs waiting to be downloaded\n"
            "q - quit\n"
        ).lower()

        if selection == "q":
            break

        elif selection == "g":
            print("All songs in the database...")
            all_songs = dao_get_all_songs()
            for song in all_songs:
                print(
                    f"Title: {song.title}, Artist: {song.artist}, Album: {song.album}, "
                    f"YouTube: {song.youtube_url}, Downloaded: {song.downloaded}, File: {song.file_path}"
                )

        elif selection == "s":
            search_query = input("Enter your search: ")
            songs = search_songs(search_query)

            if len(songs) > 0:
                print(f"Songs returned: {len(songs)}")
                for i, song in enumerate(songs, start=1):
                    print(f"{i}: Title: {song.title} Artist: {song.artist}")

                save_choice = input("Do you want to save these songs to the database? (y/n): ").lower()
                if save_choice == "y":
                    dao_save_song(songs)
                    print("Songs saved.")
                else:
                    print("Songs not saved")
            else:
                print("No songs found for your query.")

        elif selection == "c":
            confirm = input("This will DELETE ALL songs. Are you sure? (y/n): ").lower()
            if confirm == "y":
                dao_clear_songs()
                print("Database cleared.")
            else:
                print("Cancelled.")

        elif selection == "p":
            playlist_url = input("Enter Spotify playlist URL (or spotify:playlist:...): ").strip()
            songs = get_playlist_tracks(playlist_url)

            if songs:
                print(f"Tracks found: {len(songs)}")
                for i, song in enumerate(songs[:20], start=1):
                    print(f"{i}: {song.title} — {song.artist}")
                if len(songs) > 20:
                    print("... (showing first 20)")

                save_choice = input("Save these songs to the database? (y/n): ").lower()
                if save_choice == "y":
                    dao_save_song(songs)
                    print("Songs saved.")
                else:
                    print("Songs not saved")
            else:
                print("No tracks found (or playlist parsing failed).")

        elif selection == "y":
            resolve_youtube_urls_for_all_pending_songs()

        elif selection == "m":
            songs = dao_get_songs_missing_youtube_url()
            if songs:
                print(f"Songs still missing YouTube URLs: {len(songs)}")
                for song in songs:
                    print(f"{song.title} — {song.artist}")
            else:
                print("All songs already have YouTube URLs.")

        elif selection == "d":
            audio_format = input("Choose format (mp3/flac) [mp3]: ").strip().lower()
            if audio_format not in ("mp3", "flac"):
                audio_format = "mp3"
            download_all_pending_songs(audio_format=audio_format)

        elif selection == "r":
            songs = dao_get_pending_download_songs()
            if songs:
                print(f"Songs waiting to be downloaded: {len(songs)}")
                for song in songs:
                    print(f"{song.title} — {song.artist} — {song.youtube_url}")
            else:
                print("No songs are waiting for download.")