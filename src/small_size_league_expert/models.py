from typing import List

from pydantic import BaseModel, Field


class Question(BaseModel):
    """A question with a list of keywords related to the question"""

    question: str = Field(..., description="The question")
    language_code: str = Field(..., description="The language code of the question")
    keywords: List[str] = Field(
        ...,
        description="The keywords related to the question",
        examples=[
            "robot",
            "field",
            "dimensions",
            "goal",
            "penalty",
            "area",
            "measurements",
        ],
    )
    technical_domains: List[str] = Field(
        ...,
        description="The technical domains related to the question",
        examples=[
            "algorithms",
            "hardware",
            "software",
            "strategy",
            "rules",
            "communication",
            "control",
        ],
    )
    sub_questions: List[str] = Field(
        ..., description="The sub-questions related to the question", max_length=3
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


class DiscordAnswer(RankResult):
    """A Discord answer.
    This is the final answer that will be sent to the Discord channel.
    It combines the answer and the references in a way that is easy to understand and read.

    <Instructions>
    - The answer should be compressed to maximum 2000 characters.
    - The answer should be correctly referenced to the sources, using the format: [resumed text from source](reference link).
    """

    markdown_answer: str = Field(
        ..., description="The answer in Markdown format for Discord"
    )

    def get_final_answer(
        self, user_mention: str | None = None, original_question: str | None = None
    ) -> str:
        """Get the final answer in Markdown format."""

        if user_mention:
            final_answer = f'**{user_mention}**: *"{original_question or self.question}"*\n\n{self.markdown_answer}'
        else:
            final_answer = self.markdown_answer

        cropped_message = "... **(truncated due to size limit)**"
        message_size_limit = 2000 - len(cropped_message)

        cropped_answer = final_answer[:message_size_limit]

        if len(final_answer) > message_size_limit:
            cropped_answer = cropped_answer + cropped_message
        return cropped_answer
