# RoboCup SSL Article Generator

This project implements a multi-agent system using CrewAI to automatically generate informative articles about the RoboCup Small Size League (SSL). The system leverages official RoboCup SSL documentation and Wikipedia to create comprehensive, technically accurate articles on various aspects of the competition.

## Features

- **Multi-agent Architecture**: Utilizes three specialized agents working collaboratively
- **RoboCup SSL Knowledge Base**: Custom CrewAI tool for fetching information from official RoboCup SSL sources
- **Wikipedia Integration**: Additional tool for supplementary information
- **API Interface**: FastAPI server for easy article generation via HTTP requests
- **Structured Output**: Articles formatted using Pydantic models for consistency
- **LLM Flexibility**: Supports both Groq (Llama3) and Google Gemini models

## System Architecture

The system consists of three main agents:

1. **Researcher Agent**: Searches official RoboCup SSL sources and Wikipedia for comprehensive information about the specified topic
2. **Writer Agent**: Creates a well-structured, technically accurate article based on the research findings
3. **Editor Agent**: Reviews and refines the article for technical accuracy, completeness, and readability

## RoboCup SSL Resources

The system accesses information from official RoboCup SSL resources:
- Official rules: https://ssl.robocup.org/rules/
- Tournament regulations: https://ssl.robocup.org/tournament-rules/
- Technical overview: https://ssl.robocup.org/technical-overview-of-the-small-size-league/
- GitHub repositories: https://github.com/orgs/RoboCup-SSL/repositories
- SSL rules and goals documentation

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system.

1. Clone this repository:
```bash
git clone https://github.com/yourusername/robocup-ssl-article-generator.git
cd robocup-ssl-article-generator
```

2. Install dependencies using UV (recommended) or pip:
```bash
# Using UV
pip install uv
uv pip install -e .

# Using pip
pip install -e .
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
  "topic": "robot limitations",
}
```

### Command Line

Generate an article directly from the command line:

```bash
python main.py "robot limitations"
```

### Example Topics

- Robot specifications and limitations
- Field dimensions and layout
- Vision system and tracking
- Referee system
- Tournament structure
- Game rules
- Communication protocols
- Team requirements

## Development

### Project Structure

- `src/small_size_league_promoter/`
  - `tools/`: Contains the RoboCup SSL and Wikipedia tools
  - `config/`: Contains YAML configuration for agents and tasks
  - `models.py`: Pydantic models for structured data
  - `crew.py`: CrewAI implementation
  - `main.py`: FastAPI server and command-line interfaces

### Adding New Features

- To add more RoboCup SSL sources: Update the `SSL_RESOURCES` dictionary in the RoboCup tool
- To modify agent behaviors: Update `config/agents.yaml`
- To modify tasks: Update `config/tasks.yaml`

## Requirements Met

- ✅ Multi-agent system using CrewAI
- ✅ Custom tools for RoboCup SSL and Wikipedia integration
- ✅ Articles with minimum 300 words
- ✅ Integration with free LLMs (Groq and Gemini)
- ✅ Pydantic models for structured output
- ✅ FastAPI interface
- ✅ Well-documented code and README

## License

This project is available under the MIT License. See the LICENSE file for details.

## Credits

This project was created using the CrewAI framework: https://docs.crewai.com/
RoboCup SSL official resources: https://ssl.robocup.org/
