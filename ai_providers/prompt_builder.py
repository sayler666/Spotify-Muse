from .protocols import PromptBuilder


class PlaylistPromptBuilder(PromptBuilder):
    def build_prompt(self, user_input: str) -> str:
        return f"""Create a playlist based on this description: {user_input}. 
        Respond ONLY in JSON format, without any additional text before or after. 
        Format: {{
            "playlist_name": "name",
            "description": "description",
            "tracks": [
                {{
                    "artist": "artist",
                    "title": "title"
                }}
            ]
        }}"""
