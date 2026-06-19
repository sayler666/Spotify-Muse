import requests
from rich.console import Console
from rich.panel import Panel
from .protocols import AIProvider, PlaylistData
from .prompt_builder import PlaylistPromptBuilder
from .response_parser import PlaylistJSONParser

console = Console()


class GptProvider(AIProvider):
    BASE_URL = "https://api.openai.com/v1/chat/completions"
    MAX_TOKENS = 1024
    DEFAULT_TIMEOUT = 30
    MIN_PROMPT_LENGTH = 10
    MAX_PROMPT_LENGTH = 300

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._available_models = [
            "gpt-4o-mini",
        ]

        self._model = self._available_models[0]
        self.prompt_builder = PlaylistPromptBuilder()
        self.response_parser = PlaylistJSONParser()

    def get_name(self) -> str:
        return "Gpt"

    def get_model(self) -> str:
        return self._model

    def set_model(self, model: str) -> None:
        if model not in self._available_models:
            raise ValueError(
                f"Invalid model: {model}. Available models: {self._available_models}"
            )
        self._model = model

    def get_available_models(self) -> list[str]:
        return self._available_models.copy()

    def generate_playlist(self, prompt: str) -> PlaylistData | None:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        if len(prompt) not in range(self.MIN_PROMPT_LENGTH, self.MAX_PROMPT_LENGTH + 1):
            raise ValueError(
                f"Prompt length must be between {self.MIN_PROMPT_LENGTH} and {self.MAX_PROMPT_LENGTH} characters"
            )

        try:
            result = self._make_api_request(prompt)["choices"][0]["message"]

            if "content" not in result:
                raise ValueError(f"No content in response. Response: {result}")

            response_text = result["content"]
            if not response_text:
                raise ValueError(f"No text in response content: {response_text}")

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
                Panel(str(e), title="[red]GPT API[/red]", border_style="red")
            )
            return None

    def _make_api_request(self, prompt: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }

        data = {
            "model": self._model,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user", 
                    "content": self.prompt_builder.build_prompt(prompt),
                }
            ],
        }

        response = requests.post(
            self.BASE_URL, 
            headers=headers,
            json=data, 
            timeout=self.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
