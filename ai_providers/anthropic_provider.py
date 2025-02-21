from typing import Optional
import requests
from rich.console import Console
from rich.panel import Panel
from .protocols import AIProvider, PlaylistData
from .prompt_builder import PlaylistPromptBuilder
from .response_parser import PlaylistJSONParser

console = Console()


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self._available_models = [
            "claude-3-haiku-20240307",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
        ]
        self._model = self._available_models[0]
        self.prompt_builder = PlaylistPromptBuilder()
        self.response_parser = PlaylistJSONParser()

    def get_name(self) -> str:
        return "Claude"

    def get_model(self) -> str:
        return self._model

    def set_model(self, model: str) -> None:
        if model not in self._available_models:
            raise ValueError(
                f"Invalid model. Available models: {self._available_models}"
            )
        self._model = model

    def get_available_models(self) -> list[str]:
        return self._available_models.copy()

    def generate_playlist(self, prompt: str) -> Optional[PlaylistData]:
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }

            data = {
                "model": self._model,
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": self.prompt_builder.build_prompt(prompt),
                    }
                ],
            }

            response = requests.post(
                self.base_url, headers=headers, json=data, timeout=30
            )

            # Handle HTTP errors
            response.raise_for_status()

            # Parse response
            result = response.json()

            if "content" not in result:
                raise ValueError("No content in response")

            content = result["content"]
            if not isinstance(content, list) or not content:
                raise ValueError("Invalid content format in response")

            response_text = content[0].get("text", "").strip()
            if not response_text:
                raise ValueError("No text in response content")

            return self.response_parser.parse_response(response_text)

        except requests.exceptions.Timeout:
            console.print(
                Panel("Request timed out", title="[red]Error[/red]", border_style="red")
            )
            return None
        except requests.exceptions.RequestException as e:
            console.print(
                Panel(str(e), title="[red]HTTP Error[/red]", border_style="red")
            )
            return None
        except Exception as e:
            console.print(
                Panel(str(e), title="[red]Claude API[/red]", border_style="red")
            )
            return None
