#!/usr/bin/env python
import sys
import warnings

import uvicorn
from dotenv import load_dotenv

from small_size_league_promoter.crew import SmallSizeLeaguePromoter

# Load environment variables
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the crew using the command line."""
    inputs = {
        'topic': sys.argv[1] if len(sys.argv) > 1 else 'robot limitations',
    }
    
    try:
        result = SmallSizeLeaguePromoter().crew().kickoff(inputs=inputs)
        print(f"RoboCup SSL article about '{inputs['topic']}' generated successfully. Result:")
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def run_api():
    """Run the FastAPI server."""
    uvicorn.run("small_size_league_promoter.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run_api()
