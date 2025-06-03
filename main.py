import argparse

from small_size_league_expert.crew import SmallSizeLeagueExpert


def main():
    parser = argparse.ArgumentParser(description="Run the article generator.")

    parser.add_argument(
        "topic", type=str, help="The topic to generate an article about"
    )

    args = parser.parse_args()

    print(f'Starting to generate article based on topic: "{args.topic}"')

    inputs = {"original_question": args.topic}

    # Run the crew and get the result
    result = SmallSizeLeagueExpert().crew().kickoff(inputs=inputs)
    print(f"result: {type(result)} {result}\n")


if __name__ == "__main__":
    main()
