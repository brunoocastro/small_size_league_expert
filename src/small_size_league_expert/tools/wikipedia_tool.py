from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class WikipediaSearchInput(BaseModel):
    """Input schema for WikipediaSearchTool."""

    query: str = Field(..., description="The search term to look up on Wikipedia.")
    language: str = Field(
        default="pt",
        description="The language code for Wikipedia (e.g., 'pt' for Portuguese).",
    )


class WikipediaSearchTool(BaseTool):
    name: str = "Wikipedia Search"
    description: str = (
        "Searches Wikipedia for information about a specific topic. "
        "Returns the extracted text from the Wikipedia article. "
        "Useful for researching factual information about various subjects."
    )
    args_schema: Type[BaseModel] = WikipediaSearchInput

    def _run(self, query: str, language: str = "en") -> str:
        """
        Fetch content from Wikipedia API based on the search query.
        Use mainly for getting general information about a topic.
        Example:
            - "Artificial Intelligence"
            - "RoboCup Small Size League"
            - "Soccer"
            - "RoboCup"
            - "RoboCup Small Size League"
            - "Computer Vision"
            - "Machine Learning"
            - "Deep Learning"
            - "Robotics"

        Args:
            query: The search term to look up on Wikipedia.
            language: The language code for Wikipedia (default: 'en' for English).

        Returns:
            String with the extracted content from Wikipedia.
        """
        try:
            # Format the URL for the Wikipedia API
            url = f"https://{language}.wikipedia.org/w/api.php"

            # Set up the parameters for the API request
            params = {
                "action": "query",
                "prop": "extracts",
                "exlimit": "1",
                "explaintext": "1",
                "titles": query,
                "format": "json",
                "utf8": "1",
                "redirects": "1",
            }

            # Make the request to the Wikipedia API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the response
            data = response.json()

            # Extract the page content
            pages = data["query"]["pages"]
            page_id = next(iter(pages))

            # Check if page exists
            if page_id == "-1":
                return f"No Wikipedia article found for '{query}'. Try a different search term."

            # Get the extracted text
            extract = pages[page_id].get("extract", "")

            print(f"\nWikipedia article for '{query}': {extract}\n")

            if not extract:
                return f"The Wikipedia article for '{query}' exists but has no extractable content."

            return extract

        except Exception as e:
            return f"Error accessing Wikipedia: {str(e)}"
