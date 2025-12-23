import os
from dotenv import load_dotenv
load_dotenv() 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from song_model import Song
from song_dao import dao_get_all_songs, dao_save_song
from db import create_tables
from typing import List, Any, Dict, Optional

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

from typing import List, Dict, Any, Optional

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
            "q - quit\n"
        )

        
        selection = selection.lower()

        if selection == "q":
            break
        elif selection == "g":
            print("All songs in the database...")
            all_songs = dao_get_all_songs()
            for song in all_songs:
                print(f"Title: {song.title}, Artist: {song.artist}, Album: {song.album}")

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
                else:
                    print("Songs not saved")
            else:
                print("No songs found for your query.")
