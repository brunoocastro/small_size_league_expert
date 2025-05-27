from typing import List

from pydantic import BaseModel, Field


class Question(BaseModel):
    """A question with a list of keywords related to the question"""

    question: str = Field(..., description="The question")
    language_code: str = Field(..., description="The language code of the question")
    keywords: List[str] = Field(..., description="The keywords related to the question")
    sub_questions: List[str] = Field(
        ..., description="The sub-questions related to the question"
    )


class Answer(BaseModel):
    """An answer with a list of references related to the answer"""

    answer: str = Field(..., description="The answer")
    references: List[str] = Field(
        ..., description="The references related to the answer"
    )


class RetrieverResult(BaseModel):
    """A retriever result."""

    results: List[Answer] = Field(..., description="The results of the retriever")


class RankedAnswer(Answer):
    """A ranked answer."""

    rank: int = Field(..., description="The rank of the answer")


class RankResult(Question):
    """A rank result."""

    ranked_answers: List[RankedAnswer] = Field(..., description="The ranked answers")


class DiscordAnswer(Question, RankedAnswer):
    """A Discord answer.
    This is the final answer that will be sent to the Discord channel.
    It combines the answer and the references in a way that is easy to understand and read.

    <Instructions>
    - The answer should be compressed to maximum 2000 characters.
    - The answer should be correctly referenced to the sources, using the format: [resumed text from source](reference link).
    """

    final_answer: str = Field(
        ..., description="The final answer that combines the answer and the references."
    )

    def format_markdown(self) -> str:
        """Format the question and answer as markdown."""
        markdown = f"Q: {self.question}\n\n"
        markdown += f"A: \n{self.answer}\n\n"
        markdown += "References:\n"
        for i, ref in enumerate(self.references, 1):
            markdown += f"- {i}. {ref}\n"
        return markdown
