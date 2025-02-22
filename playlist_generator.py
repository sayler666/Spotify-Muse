import json
import os
import sys
from typing import Optional
from ai_providers.protocols import AIProvider
from spotify_client import SpotifyClient
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeRemainingColumn,
)
from rich.console import Console

console = Console(force_terminal=True)


class PlaylistGenerator:
    def __init__(self, spotify_client: SpotifyClient, ai_provider: AIProvider):
        self.spotify = spotify_client
        self.ai = ai_provider

    def generate(
        self, prompt: str, private: bool = False, debug: bool = False
    ) -> str | None:
        """Generate playlist and return its URL."""
        with console.status(
            f"[bold green]Generating playlist using {self.ai.get_name()} ({self.ai.get_model()})..."
        ):
            # Get AI suggestions
            playlist_data = self.ai.generate_playlist(prompt)
            if playlist_data is None:
                return None

            if debug:
                console.print(f"\n[cyan]{self.ai.get_name()} Response:[/cyan]")
                console.print(json.dumps(playlist_data, indent=2, ensure_ascii=False))

            # Create playlist
            playlist = self.spotify.create_playlist(
                name=playlist_data["playlist_name"],
                description=playlist_data["description"],
                public=not private,
            )

            if playlist is None:
                console.print("[red]Failed to create playlist.")
                return None

            track_ids = []
            not_found = []

            # Search and add tracks
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(
                    "[cyan]Searching for tracks...", total=len(playlist_data["tracks"])
                )

                for track in playlist_data["tracks"]:
                    result = self.spotify.search_track(track["artist"], track["title"])
                    if result:
                        track_ids.append(result.id)
                        console.print(
                            f"[green]✓[/green] Found: {result.artist} - {result.name}"
                        )
                    else:
                        not_found.append(f"{track['artist']} - {track['title']}")
                        console.print(
                            f"[red]✗[/red] Not found: {track['artist']} - {track['title']}"
                        )
                    progress.advance(task)

            # Add tracks to playlist
            if track_ids:
                success = self.spotify.add_tracks_to_playlist(playlist["id"], track_ids)
                if success:
                    # Convert web URL to Spotify URI
                    spotify_url = playlist["external_urls"]["spotify"]
                    spotify_uri = "spotify:" + spotify_url.split("spotify.com/")[
                        1
                    ].replace("/", ":")

                    try:
                        # Open in Spotify app
                        if sys.platform.startswith("win"):
                            os.startfile(spotify_uri)
                        elif sys.platform.startswith("darwin"):
                            os.system(f"open {spotify_uri}")
                        elif sys.platform.startswith("linux"):
                            os.system(f"xdg-open {spotify_uri}")

                        console.print(f"\n[green]Created playlist and opened in Spotify!")
                        console.print(f"[dim]Browser URL: {spotify_url}")
                        console.print(f"[dim]Spotify URI: {spotify_uri}")
                    except Exception as e:
                        console.print(f"[red]Error opening playlist: {str(e)}[/red]")
                        if debug:
                            console.print(f"\n[cyan]Platform: {sys.platform}[/cyan]")

                    if not_found:
                        console.print("\n[yellow]The following tracks were not found:")
                        for track in not_found:
                            console.print(f"[yellow]- {track}")

                    return spotify_url
            else:
                console.print("[red]No tracks were found. Playlist was not created.")
                return None
