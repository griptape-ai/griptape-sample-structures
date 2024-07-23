from griptape.config import (
    AnthropicStructureConfig,
    StructureConfig,
    GoogleStructureConfig,
    OpenAiStructureConfig,
)
from griptape.structures import Agent
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener
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
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key


def get_config(provider):
    if provider == "openai":
        return OpenAiStructureConfig()
    if provider == "anthropic":
        return AnthropicStructureConfig()
    if provider == "google":
        return GoogleStructureConfig()


def get_agent(
    config: StructureConfig, event_driver: Optional[GriptapeCloudEventListenerDriver]
):
    return Agent(
        config=config,
        event_listeners=[EventListener(driver=event_driver)],
    )


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

    config = get_config(provider)
    agent = get_agent(config, event_driver)

    result = agent.run(f"Briefly explain how { subject } work to { audience }.")
