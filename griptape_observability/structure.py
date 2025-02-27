import argparse

from griptape.structures import Agent
from griptape.utils import GriptapeCloudStructure

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prompt",
        default="What is the air speed velocity of an unladen swallow?",
        help="Specify this to run the Griptape agent with a custom prompt",
    )

    args = parser.parse_args()
    prompt = args.prompt

    with GriptapeCloudStructure(observe=True):
        Agent().run(prompt)
