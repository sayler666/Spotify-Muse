from typing import Optional, Any
import json
from rich.console import Console
from .protocols import JSONResponseParser, PlaylistData

console = Console()


class PlaylistJSONParser(JSONResponseParser):
    def parse_response(self, response_text: str) -> PlaylistData | None:
        try:
            # Strip markdown code fences if present
            text = response_text.strip()
            if text.startswith("```"):
                text = text.split("```", 2)[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.rsplit("```", 1)[0].strip()
            data = json.loads(text)
            # Basic validation of required fields
            if not all(
                key in data for key in ["playlist_name", "description", "tracks"]
            ):
                console.print("[red]Missing required fields in JSON response[/red]")
                return None

            if not isinstance(data["tracks"], list):
                console.print("[red]Tracks must be a list[/red]")
                return None

            # Validate each track
            for track in data["tracks"]:
                if not all(key in track for key in ["artist", "title"]):
                    console.print("[red]Invalid track format in response[/red]")
                    return None

            return data

        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing JSON response: {str(e)}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Unexpected error parsing response: {str(e)}[/red]")
            return None
