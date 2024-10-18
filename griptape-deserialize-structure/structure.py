import os
import json
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.configs import Defaults
from griptape.drivers import GriptapeCloudConversationMemoryDriver
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener, EventBus
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


def deserialize_agent(agent_dict: dict) -> Agent:
    """Takes a serialized JSON string and deserializes it to an Agent instance."""

    return Agent.from_dict(agent_dict)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Deserialize an agent and run it.")
    parser.add_argument(
        "--serialized",
        required=True,
        help="Serialized JSON structure of the agent",
    )
    parser.add_argument(
        "--prompt",
        default="Hello there!",
        help="The prompt you wish to use for the deserialized agent",
    )
    parser.add_argument(
        "--stream",
        default=False,
        action="store_true",
        help="Enable streaming mode for the Agent",
    )

    args = parser.parse_args()
    serialized = args.serialized
    prompt = args.prompt
    thread_id = args.thread_id
    stream = args.stream

    # Load the environment variables
    load_dotenv()

    # Deserializing the agent from the serialized input
    agent = deserialize_agent(serialized)

    # Managed environment setup
    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
        EventBus.add_event_listeners(
            [
                EventListener(
                    driver=event_driver,
                ),
            ]
        )

    # Setting up conversation memory driver with thread ID
    Defaults.drivers_config.conversation_memory_driver = (
        GriptapeCloudConversationMemoryDriver(
            api_key=get_listener_api_key(),
            thread_id=thread_id,
        )
    )

    # Running the deserialized agent
    result = agent.run(prompt)

    # Print the result
    print(f"Agent result: {result}")