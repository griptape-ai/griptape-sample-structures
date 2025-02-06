import argparse
import os

from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.configs.drivers import DriversConfig
from griptape.drivers import (
    AnthropicPromptDriver,
    GriptapeCloudEventListenerDriver,
    OpenAiEmbeddingDriver,
    LocalVectorStoreDriver
)
from griptape.events import EventBus, EventListener
from griptape.structures import Agent
from griptape.tools import PromptSummaryTool, WebScraperTool


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


def on_prompt_agent() -> Agent:
    return Agent(
        tools=[WebScraperTool()],  # default behavior is off_prompt=False
    )


def off_prompt_agent() -> Agent:
    return Agent(
        tools=[
            WebScraperTool(off_prompt=True),
            PromptSummaryTool(),
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--off_prompt",
        action="store_true",
        help="Specify this to use the off prompt Griptape agent",
    )
    parser.add_argument(
        "-w",
        "--website",
        default="https://www.griptape.ai/blog/the-power-of-task-memory-and-off-prompt-tm",
        help="specify the website to summarize into a text",
    )

    args = parser.parse_args()
    website = args.website

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
        EventBus.add_event_listener(EventListener(event_listener_driver=event_driver))
    else:
        load_dotenv()

    Defaults.drivers_config = DriversConfig(
        prompt_driver=AnthropicPromptDriver(
            model="claude-3-sonnet-20240229",
            api_key=os.environ["ANTHROPIC_API_KEY"],
        ),
        vector_store_driver=LocalVectorStoreDriver(
            embedding_driver=OpenAiEmbeddingDriver()
        ),
    )

    agent = off_prompt_agent() if args.off_prompt else on_prompt_agent()

    result = agent.run(
        f"Summarize the following website into a text message you would send a friend limited to 160 characters: { website }"
    )


