# RoboCup Small Size League Promoter - AI Powered Article Generator

This project implements a multi-agent system using CrewAI to automatically generate informative articles about the RoboCup Small Size League (SSL). The system leverages official RoboCup SSL documentation and Wikipedia to create comprehensive, technically accurate articles on various aspects of the competition.

## Demo

Public API available at: https://ssl.otone.tech/

## Features

- **Multi-agent Architecture**: Utilizes multiple specialized agents working collaboratively
- **Wikipedia Integration**: Additional tool for supplementary information
- **RoboCup SSL Knowledge Base**: Custom CrewAI tool for fetching information from official RoboCup SSL sources
- **API Interface**: FastAPI server for easy article generation via HTTP requests
- **Structured Output**: Articles formatted using Pydantic models for consistency
- **LLM Flexibility**: Supports any LLM model supported by CrewAI

### Future Features
- **MCP Integration**: Additional tool for fetching information from [Small Size League MCP](https://github.com/brunoocastro/small-size-league-mcp)

## System Architecture

The system consists of multiple specialized agents working collaboratively:

1. **Analyst Agent**: Analyzes the topic and determines the best approach for generating an article
2. **Researcher Agent**: Searches official RoboCup SSL sources and Wikipedia for comprehensive information about the specified topic
3. **Writer Agent**: Creates a well-structured, technically accurate article based on the research findings
4. **Editor Agent**: Reviews and refines the article for technical accuracy, completeness, and readability

## Installation

Ensure you have:
-  Python >=3.10 <3.13 installed on your system.
-  An API key for your LLM provider.
-  [UV](https://docs.astral.sh/uv/getting-started/installation/) installed on your system.

1. Clone this repository:
```bash
git clone https://github.com/brunoocastro/small_size_league_promoter
cd small_size_league_promoter
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate
uv sync
```

3. Set up environment variables by creating a `.env` file with:
```
MODEL=groq/llama3-8b-8192
```

You need to also add the API key for your LLM provider to the `.env` file. In this example, we're using Groq. So we need to add the following:
```
GROQ_API_KEY=your_groq_api_key_here
```

> If you're using Gemini, you need to add the following:
> ```
> MODEL=google/gemini-1.5-flash
> GOOGLE_API_KEY=your_google_api_key_here
> ```

## Usage

### Command Line execution

The command line execution is the simplest way to generate an article.
You just need to provide the topic you want to write about and the system will generate an article.

```bash
python main.py <TOPIC>
```

for example:
```bash
python main.py "Robot specifications and limitations"
```

#### Example Topics

- Robot specifications and limitations
- Field dimensions and layout
- Vision system and tracking
- Referee system
- Tournament structure
- Game rules
- Communication protocols
- Team requirements

### API Server

Run the FastAPI server with:

```bash
fastapi run api.py
```

This starts the API server at http://localhost:8000

#### API Endpoints

- `GET /`: Basic information about the API
- `POST /generate-article`: Generate an article about a RoboCup SSL topic

Example request:
```json
{
  "topic": "Vision system and tracking",
}
```

## Development

### Project Structure

- `main.py`: Command line interface
- `api.py`: FastAPI server
- `src/small_size_league_promoter/`
  - `tools/`: Contains the RoboCup SSL and Wikipedia tools
  - `config/`: Contains YAML configuration for agents and tasks
  - `models.py`: Pydantic models for structured data
  - `crew.py`: CrewAI implementation
  - `main.py`: CrewAI run script

### Adding New Features

- To modify agent behaviors: Update `config/agents.yaml`
- To modify tasks: Update `config/tasks.yaml`
- To add new tools: Create a new Python file in `src/small_size_league_promoter/tools/` and update `crew.py` to include it

## Requirements Met

- ✅ Multi-agent system using CrewAI
- ✅ Custom tools for RoboCup SSL and Wikipedia integration
- ✅ Articles with minimum 300 words
- ✅ Integration with free LLMs (Groq and Gemini)
- ✅ Pydantic models for structured output
- ✅ FastAPI interface
- ✅ Well-documented code and README
- ✅ Docker containerization
- ✅ Command line interface

Next goal is to add MCP integration.

## License

This project is available under the MIT License. See the LICENSE file for details.

## Credits

This project was created using the CrewAI framework: https://docs.crewai.com/
RoboCup SSL official resources: https://ssl.robocup.org/
