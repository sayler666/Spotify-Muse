from typing import Protocol, TypedDict, runtime_checkable


class Track(TypedDict):
    artist: str
    title: str


class PlaylistData(TypedDict):
    playlist_name: str
    description: str
    tracks: list[Track]


@runtime_checkable
class PromptBuilder(Protocol):
    """Protocol for building prompts"""

    def build_prompt(self, user_input: str) -> str:
        """Build a prompt from user input"""
        ...


@runtime_checkable
class JSONResponseParser(Protocol):
    """Protocol for parsing JSON responses"""

    def parse_response(self, response_text: str) -> PlaylistData | None:
        """Parse response text into structured data"""
        ...


@runtime_checkable
class AIProvider(Protocol):
    """Protocol defining interface for AI providers"""

    def generate_playlist(self, prompt: str) -> PlaylistData | None:
        """Generate a playlist based on the provided prompt"""
        ...

    def get_name(self) -> str:
        """Get provider name"""
        ...

    def get_model(self) -> str:
        """Get current model name"""
        ...

    def set_model(self, model: str) -> None:
        """Set model to use"""
        ...

    def get_available_models(self) -> list[str]:
        """Get list of available models"""
        ...
