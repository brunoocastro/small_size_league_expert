from typing import List, Optional, Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class TDPSearchInput(BaseModel):
    """Input schema for TDPSearchTool."""

    query: str = Field(..., description="The search query to look up in TDP.")
    leagues: str = Field(
        default="soccer_smallsize",
        description="The leagues to search in. Defaults to soccer_smallsize.",
    )


class TDPLeague(BaseModel):
    """League type for TDPSearchTool."""

    league_major: Optional[str] = Field(..., description="The major league of the TDP.")
    league_minor: Optional[str] = Field(..., description="The minor league of the TDP.")
    league_sub: Optional[str] = Field(..., description="The sub league of the TDP.")
    name: Optional[str] = Field(..., description="The name of the TDP.")
    name_pretty: Optional[str] = Field(..., description="The pretty name of the TDP.")


class TDPTeam(BaseModel):
    """Team type for TDPSearchTool."""

    name: Optional[str] = Field(..., description="The name of the team.")
    name_pretty: Optional[str] = Field(..., description="The pretty name of the team.")


class TDPInfo(BaseModel):
    """Data type for TDPSearchTool."""

    index: Optional[int] = Field(..., description="The index of the TDP.")
    league: Optional[TDPLeague] = Field(..., description="The league of the TDP.")
    team_name: Optional[TDPTeam] = Field(..., description="The team of the TDP.")
    year: Optional[int] = Field(..., description="The year of the TDP.")


class TDPResultParagraph(BaseModel):
    """Paragraph type for TDPSearchTool."""

    tdp_name: Optional[TDPInfo] = Field(
        ..., description="The TDP name information including league and team details."
    )
    title: Optional[str] = Field(..., description="The title of the paragraph.")
    content: Optional[str] = Field(..., description="The content of the paragraph.")
    questions: Optional[List[str]] = Field(
        default_factory=list,
        description="List of questions related to the paragraph content.",
    )


class TDPResult(BaseModel):
    """Response type for TDPSearchTool."""

    keywords: Optional[List[str]] = Field(
        default_factory=list, description="The keywords found in the TDP."
    )
    paragraphs: Optional[List[TDPResultParagraph]] = Field(
        default_factory=list, description="The paragraphs found in the TDP."
    )

    def pretty_markdown(self, amount_of_paragraphs: int = 5):
        """Convert the TDPResult to a pretty markdown string."""
        markdown = f"# TDP Search Results ({len(self.paragraphs)} paragraphs)\n\n"
        markdown += f"## Keywords: {', '.join(self.keywords)}\n\n"
        markdown += "## Paragraphs found:\n\n"

        for index, paragraph in enumerate(self.paragraphs[:amount_of_paragraphs]):
            markdown += f"### {index + 1}. {paragraph.tdp_name.year} TDP from {paragraph.tdp_name.team_name.name_pretty}  Team - {paragraph.title}\n\n"
            markdown += f"**Content:**\n\n{paragraph.content}\n\n"
            markdown += "- **Questions related to the content:**\n"
            for question in paragraph.questions:
                markdown += f"  - {question}\n"
            markdown += "\n"

        return markdown


class TDPSearchTool(BaseTool):
    """
    Tool for searching the TDP (Team Description Paper) for relevant information about small size league soccer projects.
    This tools calls the API provided at https://tdpsearch.com/ for the RoboTeamTwente open source project.
    The API is a simple HTTP GET request to the API endpoint with the query and leagues parameters.
    Project is open source and available at https://github.com/emielsteerneman/TDP
    """

    name: str = "TDP Search"
    description: str = (
        "Searches the TDP (Team Description Paper) for relevant information "
        "about small size league soccer projects. Useful for finding technical"
        "documentation, specifications, improvements and related information."
    )
    args_schema: Type[BaseModel] = TDPSearchInput

    def _run(self, query: str, leagues: str = "soccer_smallsize") -> str:
        # URL to the TDP search API
        base_url = "https://functionapp-test-dotenv-310.azurewebsites.net/api/query"
        params = {"query": query, "leagues": leagues}

        try:
            # Request to the TDP search API
            response = requests.get(base_url, params=params)

            # Raise an exception if the response is not successful
            response.raise_for_status()

            # Parse the JSON response
            json_response = response.json()

            print(f"JSON response: {json_response}")

            # Create a TDPResult object from the JSON response
            result = TDPResult(**json_response)

            # Print the TDP search result in a pretty markdown format
            print(f"\nTDP search result: \n{result.pretty_markdown()}\n")

            # Return the TDP search result in a pretty markdown format
            return result.pretty_markdown()
        except requests.exceptions.RequestException as e:
            # Return an error message if the TDP search API request fails
            return f"Error performing TDP search: {str(e)}"
