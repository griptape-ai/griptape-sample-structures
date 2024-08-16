import os
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.config import config
from griptape.drivers.memory.conversation.griptape_cloud_conversation_memory_driver import (
    GriptapeCloudConversationMemoryDriver,
)
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener, event_bus
import argparse


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_base_url() -> str:
    return os.environ.get("GT_CLOUD_BASE_URL", "https://cloud.griptape.ai")


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if is_running_in_managed_environment() and not api_key:
        print(
            """
              ****WARNING****: No value was found for the 'GT_CLOUD_API_KEY' environment variable.
              This environment variable is required when running in Griptape Cloud for authorization.
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prompt",
        default="Hello there!",
        help="The prompt you wish to use",
    )
    parser.add_argument(
        "-t",
        "--thread_id",
        default=None,
        help="The Griptape Cloud Thread ID you wish to use",
    )

    args = parser.parse_args()
    prompt = args.prompt
    thread_id = args.thread_id

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
        event_bus.add_event_listeners(
            [
                EventListener(
                    # By default, GriptapeCloudEventListenerDriver uses the api key provided
                    # in the GT_CLOUD_API_KEY environment variable.
                    driver=event_driver,
                ),
            ]
        )
    else:
        load_dotenv()
        event_driver = None

    config.drivers.conversation_memory = GriptapeCloudConversationMemoryDriver(
        base_url=get_base_url() + "/api",
        api_key=get_listener_api_key(),
        id=thread_id,
    )

    agent = Agent()

    result = agent.run(prompt)
