import argparse
import os

from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.configs.drivers import DriversConfig
from griptape.drivers import (
    AnthropicPromptDriver,
    LocalVectorStoreDriver,
    OpenAiEmbeddingDriver,
)
from griptape.structures import Agent
from griptape.tools import PromptSummaryTool, WebScraperTool
from griptape.utils import GriptapeCloudStructure

load_dotenv()


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

    Defaults.drivers_config = DriversConfig(
        prompt_driver=AnthropicPromptDriver(
            model="claude-3-sonnet-20240229",
            api_key=os.environ["ANTHROPIC_API_KEY"],
        ),
        vector_store_driver=LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver()),
    )

    agent = off_prompt_agent() if args.off_prompt else on_prompt_agent()

    with GriptapeCloudStructure():
        agent.run(f"Summarize the following website into a brief text message you would send a friend: {website}")
