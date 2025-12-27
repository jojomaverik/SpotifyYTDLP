import os
import re
from typing import List, Dict, Any, Optional

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from song_model import Song


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

def extract_playlist_id(playlist_input: str) -> Optional[str]:
    if playlist_input.startswith("spotify:playlist:"):
        return playlist_input.split(":")[-1].strip()

    m = re.search(r"open\.spotify\.com/playlist/([a-zA-Z0-9]+)", playlist_input)
    if m:
        return m.group(1)

    if re.fullmatch(r"[a-zA-Z0-9]{16,}", playlist_input.strip()):
        return playlist_input.strip()

    return None


def get_playlist_tracks(playlist_input: str) -> List[Song]:
    playlist_id = extract_playlist_id(playlist_input)
    if not playlist_id:
        print("Could not parse playlist id from input.")
        return []

    songs: List[Song] = []
    offset = 0
    limit = 100  # Spotify allows up to 100 per request for playlist_items

    while True:
        results = sp.playlist_items(
            playlist_id,
            offset=offset,
            limit=limit,
            additional_types=("track",),
        )
        if not results:
            break



        items = results.get("items", [])
        for item in items:
            track = item.get("track")
            if not track:
                continue  # removed/unavailable track

            # Some playlists include "local" tracks without Spotify IDs
            spotify_id = track.get("id")
            if not spotify_id:
                continue

            title = track.get("name")
            artists = track.get("artists") or []
            artist_name = artists[0].get("name") if artists else "Unknown Artist"
            album = (track.get("album") or {}).get("name", "Unknown Album")

            songs.append(
                Song(
                    title=title,
                    artist=artist_name,
                    album=album,
                    spotify_id=spotify_id,
                )
            )

        if not results.get("next"):
            break

        offset += limit

    return songs
