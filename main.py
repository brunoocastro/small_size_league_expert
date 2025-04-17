import argparse

from small_size_league_promoter.crew import SmallSizeLeaguePromoter


def main():
    parser = argparse.ArgumentParser(description='Run the article generator.')

    parser.add_argument('topic', type=str, help='The topic to generate an article about')

    args = parser.parse_args()

    print(f'Starting to generate article based on topic: "{args.topic}"')

    inputs = {
        "topic": args.topic
    }

    # Run the crew and get the result
    result = SmallSizeLeaguePromoter().crew().kickoff(inputs=inputs)
    print(f"result: {type(result)} {result}\n")

if __name__ == "__main__":
    main()
