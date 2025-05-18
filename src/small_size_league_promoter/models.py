from typing import List

from pydantic import BaseModel, Field


class ArticleSection(BaseModel):
    """A section of the article with a title and content."""

    title: str = Field(..., description="The title of the section")
    content: str = Field(..., description="The content text of the section")


class Article(BaseModel):
    """A complete article with metadata and content."""

    topic: str = Field(..., description="The main topic of the article")
    title: str = Field(..., description="The title of the article")
    summary: str = Field(..., description="A short summary of the article")
    tldr: List[str] = Field(..., description="A bullet point summary of the article")
    sections: List[ArticleSection] = Field(
        ..., description="List of sections that make up the article"
    )
    references: List[str] = Field(
        default_factory=list, description="List of references used in the article"
    )

    def format_markdown(self) -> str:
        """Format the article as markdown."""
        markdown = f"# {self.title}\n\n"
        markdown += f"## Summary\n{self.summary}\n\n"
        markdown += f"## TL;DR\n{self.tldr}\n\n"
        for section in self.sections:
            markdown += f"## {section.title}\n{section.content}\n\n"

        if self.references:
            markdown += "## References\n"
            for i, ref in enumerate(self.references, 1):
                markdown += f"{i}. {ref}\n"

        return markdown


class QuestionAnswer(BaseModel):
    """A question and answer."""

    question: str = Field(..., description="The question")
    answer: str = Field(..., description="The answer")
    references: List[str] = Field(..., description="The references")
