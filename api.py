
# FastAPI app definition
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from small_size_league_promoter.crew import SmallSizeLeaguePromoter
from small_size_league_promoter.models import Article

app = FastAPI(
    title="RoboCup SSL Article Generator API",
    description="API for generating articles about RoboCup Small Size League using CrewAI",
    version="1.0.0",
    docs_url="/"
)

class ArticleRequest(BaseModel):
    """Request model for article generation.
    
    Args:
        topic: The topic of the article to generate.

    Example of topics:
        - Vision system and tracking
        - Robot limitations
        - Field specifications
        - Referee system
        - Tournament structure
    """
    topic: str

class ArticleResponse(BaseModel):
    """Response model for article generation."""
    article: Article
    markdown: str
    success: bool
    message: str

@app.post("/generate-article", response_model=ArticleResponse, )
async def generate_article(request: ArticleRequest):
    """Generate an article about the specified RoboCup SSL topic."""
    try:
        # Configure inputs for the crew
        inputs = {
            'topic': request.topic,
        }
        
        # Initialize the crew with the specified LLM choice
        crew_instance = SmallSizeLeaguePromoter()
        
        # Run the crew and get the result
        result = crew_instance.crew().kickoff(inputs=inputs)
        print(f"result: {type(result)} {result}\n")
        article = result.pydantic
        print(f"\n Article tldr: {type(article)} {article.tldr}")


        # Parse the markdown result into the Article model
        # For simplicity, we're returning the raw result and success info
        return ArticleResponse(
            article=article,  # Assuming the crew returns an Article instance
            markdown=article.format_markdown(),
            success=True,
            message=f"Successfully generated article about {request.topic} in RoboCup SSL"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating article: {str(e)}"
        )