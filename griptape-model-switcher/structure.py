from griptape.config import config
from griptape.config.drivers import (
    AnthropicDriverConfig,
    GoogleDriverConfig,
    OpenAiDriverConfig,
)
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import event_bus, EventListener
from griptape.structures import Agent
from typing import Optional
import os
import argparse
from dotenv import load_dotenv


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if is_running_in_managed_environment() and not api_key:
        print(
            """
              ****WARNING****: No value was found for the 'GT_CLOUD_API_KEY' environment variable.
              This environment variable is required when running in Griptape Cloud for authorization.
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/configuration/api-keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key


def get_config(provider):
    if provider == "openai":
        return OpenAiDriverConfig()
    if provider == "anthropic":
        return AnthropicDriverConfig()
    if provider == "google":
        return GoogleDriverConfig()


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
    else:
        load_dotenv()
        event_driver = None

    # If we're using an event driver, ensure its events go to the global event bus.
    event_bus.add_event_listener(EventListener(driver=event_driver))

    config = get_config(provider)
    agent = Agent()

    result = agent.run(f"Briefly explain how { subject } work to { audience }.")
