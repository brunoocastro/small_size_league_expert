import os
from typing import Type

from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from pydantic import BaseModel, Field


class SSLMCPToolInput(BaseModel):
    """Input schema for SSL MCP Tool."""

    query: str = Field(..., description="Query to search for in the TDP database")


# TODO: Finish the MCP integration for the SSL MCP Tool - Launched a few days ago, few docs. On Development...
class SSLMCPTool(BaseTool):
    """Searches the RoboCup Small Size League (SSL) MCP for relevant information from SSL Site, Rules and Goals."""

    name: str = "SSL MCP Tool"
    description: str = "Searches the RoboCup Small Size League (SSL) MCP for relevant information from SSL Site, Rules and Goals."
    args_schema: Type[BaseModel] = SSLMCPToolInput

    serverparams = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "--with",
            "mcp",
            "mcp",
            "run",
            # f"{settings.mcp_path}"
        ],
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
