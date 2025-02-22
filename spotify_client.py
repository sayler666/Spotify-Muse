from dataclasses import dataclass
from typing import List, Optional
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich.console import Console
from config import SpotifyConfig

console = Console(force_terminal=True)


@dataclass
class SpotifyTrack:
    id: str
    name: str
    artist: str


class SpotifyClient:
    def __init__(self, config: SpotifyConfig):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.redirect_uri,
                scope="playlist-modify-public playlist-modify-private",
            )
        )
        self.user_id = self.sp.current_user()["id"]

    def create_playlist(
        self, name: str, description: str = "", public: bool = True
    ) -> dict | None:
        try:
            return self.sp.user_playlist_create(
                user=self.user_id, name=name, public=public, description=description
            )
        except Exception as e:
            console.print(f"[red]Error creating playlist: {str(e)}")
            return None

    def search_track(self, artist: str, title: str) -> SpotifyTrack | None:
        try:
            query = f"artist:{artist} track:{title}"
            results = self.sp.search(q=query, limit=1, type="track")

            if not results or "tracks" not in results:
                return None

            tracks = results["tracks"]["items"]
            if not tracks:
                return None

            track = tracks[0]
            return SpotifyTrack(
                id=track["id"], name=track["name"], artist=track["artists"][0]["name"]
            )

        except Exception as e:
            console.print(f"[red]Error searching for track: {str(e)}")
            return None

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str]) -> bool:
        try:
            if track_ids:
                self.sp.playlist_add_items(playlist_id, track_ids)
                return True
            return False
        except Exception as e:
            console.print(f"[red]Error adding tracks to playlist: {str(e)}")
            return False
