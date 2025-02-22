from dataclasses import dataclass
from pathlib import Path
import configparser
from rich.console import Console
import sys

console = Console()


@dataclass
class SpotifyConfig:
    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass
class AIConfig:
    provider: str
    api_key: str
    model: str


@dataclass
class AppConfig:
    spotify: SpotifyConfig
    ai: AIConfig


SCRIPT_DIR = Path(__file__).parent.absolute()
CONFIG_DIR = SCRIPT_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "config.ini"


def setup_directories() -> None:
    """Create necessary directories if they don't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def create_default_config() -> None:
    """Create default configuration file."""
    config = configparser.ConfigParser()
    config["spotify"] = {
        "client_id": "",
        "client_secret": "",
        "redirect_uri": "http://localhost:8888/callback",
    }
    config["ai"] = {"provider": "anthropic", "api_key": "", "model": ""}

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)


def load_config() -> AppConfig:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        create_default_config()
        console.print(f"[yellow]Created default config file at: {CONFIG_FILE}")
        console.print("[red]Please fill in your API keys and credentials.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")

    try:
        return AppConfig(
            spotify=SpotifyConfig(
                client_id=config["spotify"]["client_id"],
                client_secret=config["spotify"]["client_secret"],
                redirect_uri=config["spotify"]["redirect_uri"],
            ),
            ai=AIConfig(
                provider=config["ai"]["provider"],
                api_key=config["ai"]["api_key"],
                model=config["ai"].get("model", ""),
            ),
        )
    except Exception as e:
        console.print(f"[red]Error in configuration file: {str(e)}")
        sys.exit(1)
