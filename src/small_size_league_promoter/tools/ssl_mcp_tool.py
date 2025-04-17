import os
from typing import Type

from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from pydantic import BaseModel, Field

from small_size_league_promoter.settings import settings


class SSLMCPToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="Query to search for in the TDP database")

class SSLMCPTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = SSLMCPToolInput

    serverparams = StdioServerParameters(
    command="uv",
    args=["run",
        "--with",
        "mcp",
        "mcp",
        "run",
        f"{settings.mcp_path}"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

    def _run(self, query: str) -> str:
        # Implementation goes here
        try:
            mcp_server_adapter = MCPServerAdapter(self.serverparams)
            tools = mcp_server_adapter.tools
            print(f"MCP tools: {tools}")
            return tools

        except Exception as e:
            return f"Error accessing MCP: {str(e)}"

        finally:
            mcp_server_adapter.close()



