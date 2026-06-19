# Spotify Muse (playlist generator)

A command-line tool that uses AI to generate personalized Spotify playlists based on text descriptions. Simply describe the kind of playlist you want, and the tool will create it in your Spotify account.

## Features

- Generate Spotify playlists using natural language descriptions
- AI-powered track selection using Anthropic Claude (more LLMs incomming)
- Automatic playlist creation in your Spotify account
- Support for private playlists
- Debug mode for troubleshooting
- Configurable AI providers and models

## Prerequisites

- pyenv (Python version management)
- Poetry (Package management)
- Python 3.11+
- Spotify Developer Account API key
- Claude API key

## Installation

1. Clone the repository
2. Install Python using pyenv:
```bash
pyenv install 3.12.0
pyenv local 3.12.0
```
3. Install Poetry:
```bash
python -m pip install poetry
```
4. Install dependencies:
```bash
poetry install
```

## Configuration

Before using the tool, you need to set up your configuration:

1. Run the configure command:
```bash
python -m spotify_muse configure
```

2. Edit the generated `config/config.ini` file with your credentials:
```ini
[spotify]
client_id = your_spotify_client_id
client_secret = your_spotify_client_secret
redirect_uri = http://localhost:8888/callback

[ai]
provider = anthropic
api_key = your_claude_api_key
model = claude-3-haiku-20240307  # optional
```

### Getting the Required Credentials

1. **Spotify Credentials**:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Get the Client ID and Client Secret
   - Add `http://localhost:8888/callback` to your Redirect URIs

2. **Claude API Key**:
   - Get your API key from [Anthropic](https://www.anthropic.com)

## Usage

### Basic Usage

Create a playlist by providing a description:

```bash
python -m spotify_muse create "A relaxing indie folk playlist perfect for a rainy Sunday morning"
```

### Advanced Options

Create a private playlist:
```bash
python -m spotify_muse create --private "Epic workout mix with high-energy electronic music"
```

Use debug mode for detailed information:
```bash
python -m spotify_muse create --debug "90s hip hop classics"
```

Override AI provider or model:
```bash
python -m spotify_muse create --ai-provider anthropic --model claude-3-opus-20240229 "Jazz fusion from the 70s"
```

## How It Works

1. Your description is sent to Claude AI which generates a curated list of songs
2. The tool searches for each song on Spotify
3. A new playlist is created with the found tracks
4. The playlist automatically opens in your Spotify app
5. Any tracks that couldn't be found are listed in the console

## Supported AI Models

Currently supported Claude models:
- claude-3-haiku-20240307
- claude-3-opus-20240229
- claude-3-sonnet-20240229

## Error Handling

- Use `--debug` flag for detailed error information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.