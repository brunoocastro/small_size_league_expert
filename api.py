# FastAPI app definition
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from small_size_league_promoter.crew import SmallSizeLeaguePromoter
from small_size_league_promoter.models import QuestionAnswer

app = FastAPI(
    title="RoboCup SSL Article Generator API",
    description="API for generating articles about RoboCup Small Size League using CrewAI",
    version="1.0.0",
    docs_url="/",
)


class QuestionRequest(BaseModel):
    """Request model for article generation.

    Args:
        question: The question to answer.

    Example of topics:
        - Vision system and tracking
        - Robot limitations
        - Field specifications
        - Referee system
        - Tournament structure
    """

    question: str


class QuestionResponse(BaseModel):
    """Response model for article generation."""

    result: QuestionAnswer
    success: bool


@app.post(
    "/generate-article",
    response_model=QuestionAnswer,
)
async def generate_article(request: QuestionRequest):
    """Generate an answer to the specified RoboCup SSL question."""
    try:
        # Configure inputs for the crew
        inputs = {
            "question": request.question,
        }

        # Initialize the crew with the specified LLM choice
        crew_instance = SmallSizeLeaguePromoter()

        # Run the crew and get the result
        result = crew_instance.crew().kickoff(inputs=inputs)
        print(f"result: {type(result)} {result}\n")
        question = result.pydantic
        print(f"\n Question tldr: {type(question)} {question.answer}")

        # Parse the markdown result into the Article model
        # For simplicity, we're returning the raw result and success info
        return QuestionResponse(
            result=result.pydantic,
            success=True,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating article: {str(e)}"
        )
