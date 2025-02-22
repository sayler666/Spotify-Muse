import click
from config import setup_directories, load_config, CONFIG_FILE
from spotify_client import SpotifyClient
from ai_providers import AIProviderFactory
from playlist_generator import PlaylistGenerator
from rich.console import Console
from typing import Optional

console = Console(force_terminal=True)


@click.group()
def spotify_muse():
    """Tool for creating Spotify playlists using AI."""
    pass


@spotify_muse.command()
@click.option("--config", is_flag=True, help="Open configuration file.")
def configure(config):
    """Configure the tool."""
    setup_directories()
    if config:
        click.edit(filename=str(CONFIG_FILE))
    else:
        console.print(f"[green]Configuration file is located at: {CONFIG_FILE}")


@spotify_muse.command()
@click.argument("prompt")
@click.option("--private", is_flag=True, help="Create a private playlist.")
@click.option("--debug", is_flag=True, help="Display detailed debug information.")
def create(prompt: str, private: bool, debug: bool):
    """Create a playlist based on the provided description."""
    setup_directories()
    config = load_config()

    provider_type = config.ai.provider
    api_key = config.ai.api_key

    try:
        ai_provider = AIProviderFactory.create_provider(provider_type, api_key)

        if config.ai.model:
            ai_provider.set_model(config.ai.model)

        spotify_client = SpotifyClient(config.spotify)
        playlist_generator = PlaylistGenerator(spotify_client, ai_provider)

        playlist_generator.generate(prompt, private, debug)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        if debug:
            console.print_exception()


if __name__ == "__main__":
    spotify_muse()
