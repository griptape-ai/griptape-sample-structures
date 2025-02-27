import argparse

from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.configs.drivers import (
    AnthropicDriversConfig,
    DriversConfig,
    GoogleDriversConfig,
    OpenAiDriversConfig,
)
from griptape.structures import Agent
from griptape.utils import GriptapeCloudStructure

load_dotenv()


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

    Defaults.drivers_config = get_config(provider)
    agent = Agent()

    with GriptapeCloudStructure():
        agent.run(f"Briefly explain how {subject} work to {audience}.")
