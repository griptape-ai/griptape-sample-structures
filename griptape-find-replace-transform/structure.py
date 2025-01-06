import argparse
import os
from griptape.structures import Agent
from griptape.events import EventBus, EventListener
from griptape.drivers import GriptapeCloudEventListenerDriver

from dotenv import load_dotenv

def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def build_agent(find_word, replace_with, artifacts):
    agent = Agent(
        input=f"Replace the word {find_word} with {replace_with} in {artifacts}"
    )

    return agent


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_artifacts")  # positional
    parser.add_argument(
        "-f",
        "--find_word",
        help="The word you wish to find in the artifacts",
    )
    parser.add_argument(
        "-r",
        "--replace_with",
        help="The word you wish to replace with",
    )

    args = parser.parse_args()

    load_dotenv()

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver()
        EventBus.add_event_listener(EventListener(event_listener_driver=event_driver))

    agent = build_agent(args.find_word, args.replace_with, args.input_artifacts)
    agent.run()

    print(agent.output)
