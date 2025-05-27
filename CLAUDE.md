# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RoboCup Small Size League (SSL) AI-powered content generation system built with CrewAI. The project contains two distinct multi-agent systems:

1. **Small Size League Expert** (`src/small_size_league_expert/`) - Question answering system optimized for Discord
2. **Small Size League Promoter** (`src/small_size_league_promoter/`) - Article generation system for comprehensive content creation

## System Architecture

### Small Size League Expert (Discord Q&A System)
**Primary Purpose**: Real-time question answering for Discord bot interactions

**Agents**:
- `language_decomposer`: Detects input language and breaks complex questions into focused sub-questions
- `retriever`: Searches SSL knowledge sources (MCP + Wikipedia) for relevant content
- `ranker`: Evaluates and ranks retrieved content by relevance and accuracy  
- `answer_generator`: Creates Discord-optimized responses with proper formatting and sourcing

**Key Features**:
- Multi-language support with automatic language detection
- Discord message size limit compliance (2000 characters)
- Inline source citations with functional links
- Emoji integration for engagement
- Structured Pydantic models: `Question`, `RetrieverResult`, `RankResult`, `DiscordAnswer`

**Workflow**: Question → Language Detection & Decomposition → Content Retrieval → Ranking → Discord Answer Generation

### Small Size League Promoter (Article Generation System)  
**Primary Purpose**: Comprehensive article creation for educational and promotional content

**Agents** (currently commented out but architecturally defined):
- `classifier`: Validates questions are SSL-related before processing
- `language_decomposer`: Language detection and question breakdown (shared functionality)
- `retriever`: Content gathering from multiple sources (shared functionality)  
- `ranker`: Content evaluation and filtering (shared functionality)
- `answer_generator`: Long-form content generation with detailed explanations

**Key Features**:
- Extensive article generation (300+ words minimum)
- Structured content with sections, summaries, and TL;DR
- Academic-style referencing
- Support for complex technical explanations
- Structured Pydantic models: `Article`, `ArticleSection`, `QuestionAnswer`

**Workflow**: Topic Classification → Content Research → Article Writing → Editorial Review

## Common Development Commands

### Environment Setup
```bash
uv venv
source .venv/bin/activate
uv sync
```

### Running Systems

**Expert System (Discord Bot)**:
```bash
make discord
# or
python discord_bot.py
```

**Promoter System (API)**:
```bash
make api
# or
fastapi run api.py --port 3000 --reload
```

**CLI Interface**:
```bash
python main.py "your question here"
```

### Docker
```bash
docker-compose up  # Runs API on port 8000
```

### Code Quality
```bash
ruff check    # Linting
ruff format   # Formatting
```

## Key Configuration Files

### Expert System
- **Agents**: `src/small_size_league_expert/config/agents.yaml`
- **Tasks**: `src/small_size_league_expert/config/tasks.yaml`  
- **Models**: `src/small_size_league_expert/models.py`

### Promoter System
- **Agents**: `src/small_size_league_promoter/config/agents.yaml`
- **Tasks**: `src/small_size_league_promoter/config/tasks.yaml`
- **Models**: `src/small_size_league_promoter/models.py`

## Environment Variables

Required in `.env` file:
- `MODEL`: LLM model (e.g., `groq/llama3-8b-8192`, `google/gemini-1.5-flash`)
- `GROQ_API_KEY` or `GOOGLE_API_KEY`: Depending on chosen model
- `DISCORD_BOT_TOKEN`: For Discord bot functionality
- `DISCORD_GUILD_ID`: Optional, for guild-specific command sync

## Technical Implementation Details

### MCP Integration
Both systems connect to an MCP server at `localhost:8000/sse` for SSL-specific knowledge retrieval. The retriever agents dynamically load MCP tools and combine them with Wikipedia search capabilities.

### Multi-Language Support
- Language detection preserves original question language
- Responses generated in the same language as input
- Translation notes included for translated sources
- Format: `"Content in original language (translated)"`

### Response Formatting

**Expert System (Discord)**:
- 2000 character limit with truncation handling
- Inline source citations: `[statement](link)`
- Emoji integration for engagement
- Question restatement at response start
- Mandatory AI disclaimer

**Promoter System (Articles)**:
- Minimum 300 words
- Structured sections with headers
- Summary and TL;DR sections
- Bibliography-style references
- Markdown formatting for web display

### Knowledge Sources
- **Primary**: MCP server with SSL-specific content
- **Secondary**: Wikipedia for general technical concepts  
- **Fallback**: Text file knowledge source (`content_description.txt`)

### Agent Temperature Settings
- **Expert**: `temperature=0` (factual accuracy priority)
- **Promoter**: `temperature=0.1` (slight creativity for article flow)

## Development Guidelines

### When to Use Which System
- **Expert**: Quick questions, Discord interactions, fact-checking, real-time support
- **Promoter**: Educational content, detailed explanations, comprehensive articles, documentation

### Testing Considerations
Both systems use sequential CrewAI processes where agent outputs cascade through the workflow. Test the complete pipeline when modifying agents or tasks, as changes can affect downstream processing.

### Discord Development
Use guild-specific configuration during development to avoid affecting production command deployment.