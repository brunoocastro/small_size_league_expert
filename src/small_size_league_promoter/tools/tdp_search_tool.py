from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class TDPSearchInput(BaseModel):
    """Input schema for TDPSearchTool."""
    query: str = Field(..., description="The search query to look up in TDP.")
    leagues: str = Field(default="soccer_smallsize", description="The leagues to search in. Defaults to soccer_smallsize.")


class TDPSearchTool(BaseTool):
    name: str = "TDP Search"
    description: str = (
        "Searches the TDP (Team Description Paper) for relevant information "
        "about small size league soccer projects. Useful for finding technical"
        "documentation, specifications, improvements and related information."
    )
    args_schema: Type[BaseModel] = TDPSearchInput

    def _run(self, query: str, leagues: str = "soccer_smallsize") -> str:
        base_url = "https://functionapp-test-dotenv-310.azurewebsites.net/api/query"
        params = {
            "query": query,
            "leagues": leagues
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error performing TDP search: {str(e)}"
