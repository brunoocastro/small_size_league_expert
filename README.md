# RoboCup Small Size League Expert - Discord Bot

This project implements an AI-powered Discord bot that answers questions about the RoboCup Small Size League (SSL). The bot uses a multi-agent system (CrewAI) to process user questions, retrieve information from official SSL sources, team description papers, and Wikipedia, and deliver well-formatted, referenced answers directly in Discord.

## Features

- **Discord Integration**: Interact with the bot using slash commands (`/ask`, `/help`, `/contact`, `/feedback`)
- **Multi-agent Architecture**: Specialized agents for language analysis, retrieval, ranking, and answer generation
- **Official SSL Knowledge Base**: Fetches information from RoboCup SSL documentation, rules, and team papers via MCP integration
- **Wikipedia Supplementation**: Uses Wikipedia for general technical concepts
- **Structured, Referenced Answers**: Answers are formatted for Discord, with citations and markdown
- **Error Handling**: Graceful error messages and troubleshooting tips for users

## How It Works

1. **User asks a question** in Discord using `/ask`.
2. The bot analyzes the question, decomposes it, and determines the best sources to consult.
3. It retrieves and ranks relevant information from SSL sources and Wikipedia.
4. The answer is synthesized, formatted, and sent back to the Discord channel.

## Installation

### Requirements

- Python >=3.10, <3.13
- [UV](https://docs.astral.sh/uv/getting-started/installation/) for dependency management
- Discord bot token
- (Optional) API keys for LLM providers (Groq, OpenAI, Gemini, etc.)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brunoocastro/small_size_league_expert.git
   cd small_size_league_expert
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. **Configure environment variables:**
   - Copy `env.example` to `.env` and fill in your credentials:
     ```
     DISCORD_BOT_TOKEN=your_discord_token_here
     MODEL=groq/llama3-8b-8192
     GROQ_API_KEY=your_groq_api_key_here
     # Or for OpenAI/Gemini, set the appropriate keys
     ```
   - (Optional) Set `MCP_ENDPOINT` if using a custom MCP server.

4. **(Optional) Run MCP server via Docker Compose:**
   ```bash
   docker compose up -d
   ```

## Usage

### Running the Discord Bot

Start the bot locally:
```bash
uv run python discord_bot.py
```
Or use the provided Makefile:
```bash
make discord
```

### Discord Commands

- `/ask <question>`: Ask any SSL-related question
- `/help`: Get information about the bot and its capabilities
- `/contact`: Contact the admin or get support info
- `/feedback`: Send feedback or suggestions

### Example Questions

- What are the official SSL field dimensions?
- How does the vision system track robots?
- What communication protocols are allowed in SSL?
- How do teams design their robot strategies?

## Development

### Project Structure

- `discord_bot.py`: Main Discord bot logic and command definitions
- `src/small_size_league_expert/crew.py`: CrewAI multi-agent system implementation
- `src/small_size_league_expert/tools/`: Custom tools for SSL and Wikipedia integration
- `src/small_size_league_expert/models.py`: Pydantic models for structured answers
- `src/small_size_league_expert/config/`: YAML configs for agents and tasks
- `bot_explanation.md`: Markdown help text for the bot

### Adding New Features

- Update or add new agents in `config/agents.yaml`
- Add new tools in `src/small_size_league_expert/tools/` and register in `crew.py`
- Adjust answer formatting or retrieval logic in `crew.py` and `models.py`

## Troubleshooting

- If the bot is unresponsive or you see heartbeat warnings, ensure no blocking code is running in the event loop.
- Check your `.env` file for correct tokens and API keys.
- Review logs for errors related to MCP server or LLM provider connectivity.

## License

This project is available under the MIT License.

## Credits

- Built with [CrewAI](https://docs.crewai.com/)
- RoboCup SSL resources: https://ssl.robocup.org/
