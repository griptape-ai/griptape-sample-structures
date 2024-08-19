from griptape.config import AnthropicStructureConfig
from griptape.drivers import AnthropicPromptDriver
from griptape.structures import Agent
from griptape.tools import TaskMemoryClient, WebScraper
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
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/configuration/api-keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key


def on_prompt_agent(event_driver: Optional[GriptapeCloudEventListenerDriver]):
    return Agent(
        config=AnthropicStructureConfig(
            prompt_driver=AnthropicPromptDriver(
                model="claude-3-5-sonnet-20240620",
                api_key=os.environ["ANTHROPIC_API_KEY"],
            ),
        ),
        event_listeners=[EventListener(driver=event_driver)],
        tools=[WebScraper()],  # default behavior is off_prompt=False
    )


def off_prompt_agent(event_driver: Optional[GriptapeCloudEventListenerDriver]):
    return Agent(
        config=AnthropicStructureConfig(
            prompt_driver=AnthropicPromptDriver(
                model="claude-3-5-sonnet-20240620",
                api_key=os.environ["ANTHROPIC_API_KEY"],
            ),
        ),
        event_listeners=[EventListener(driver=event_driver)],
        tools=[
            WebScraper(off_prompt=True),
            TaskMemoryClient(),
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
    else:
        load_dotenv()
        event_driver = None

    agent = (
        off_prompt_agent(event_driver)
        if args.off_prompt
        else on_prompt_agent(event_driver)
    )

    result = agent.run(
        f"Summarize the following website into a text message you would send a friend limited to 160 characters: { website }"
    )
