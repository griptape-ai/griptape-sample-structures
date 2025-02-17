import argparse
import os

from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.configs.drivers import (
    AnthropicDriversConfig,
    DriversConfig,
    GoogleDriversConfig,
    OpenAiDriversConfig,
)
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventBus, EventListener
from griptape.structures import Agent


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if is_running_in_managed_environment() and not api_key:
        pass
    return api_key


def get_config(provider: str) -> DriversConfig | None:
    if provider == "openai":
        return OpenAiDriversConfig()
    if provider == "anthropic":
        return AnthropicDriversConfig()
    if provider == "google":
        return GoogleDriversConfig()
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--provider",
        choices=["openai", "anthropic", "google"],
        default="google",
        help="List the provider for the model you want to use. Must be 'openai', 'anthropic', or 'google'",
    )
    parser.add_argument(
        "-s",
        "--subject",
        default="computers",
        help="The subject you wish to explain",
    )
    parser.add_argument(
        "-a",
        "--audience",
        default="a five-year-old child",
        help="The audience you wish to explain *to*",
    )

    args = parser.parse_args()
    provider = args.provider
    subject = args.subject
    audience = args.audience

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
        EventBus.add_event_listener(EventListener(event_listener_driver=event_driver))
    else:
        load_dotenv()

    Defaults.drivers_config = get_config(provider)
    agent = Agent()

    result = agent.run(f"Briefly explain how {subject} work to {audience}.")
