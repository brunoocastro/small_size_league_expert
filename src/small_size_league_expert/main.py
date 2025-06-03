#!/usr/bin/env python
import sys
import warnings

from dotenv import load_dotenv

from small_size_league_expert.crew import SmallSizeLeagueExpert

# Load environment variables
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """Run the crew using the command line."""
    inputs = {
        "topic": sys.argv[1] if len(sys.argv) > 1 else "robot limitations",
    }

    try:
        result = SmallSizeLeagueExpert().crew().kickoff(inputs=inputs)
        print(
            f"RoboCup SSL article about '{inputs['topic']}' generated successfully. Result:"
        )
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
