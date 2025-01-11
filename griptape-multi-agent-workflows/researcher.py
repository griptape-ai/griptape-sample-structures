import os
import sys

from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.tools import (
    PromptSummaryTool,
    WebScraperTool,
    WebSearchTool,
)
from griptape.drivers import GoogleWebSearchDriver, GriptapeCloudEventListenerDriver
from griptape.events import EventBus, EventListener


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if not api_key:
        print(
            """
              ****WARNING****: No value was found for the 'GT_CLOUD_API_KEY' environment variable.
              This environment variable is required when running in Griptape Cloud for authorization.
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key


def build_researcher():
    """Builds a Researcher Structure."""
    researcher = Agent(
        id="researcher",
        tools=[
            WebSearchTool(
                web_search_driver=GoogleWebSearchDriver(
                    api_key=os.environ["GOOGLE_API_KEY"],
                    search_id=os.environ["GOOGLE_API_SEARCH_ID"],
                ),
            ),
            WebScraperTool(
                off_prompt=True,
            ),
            PromptSummaryTool(),
        ],
        rulesets=[
            Ruleset(
                name="Position",
                rules=[
                    Rule(
                        value="Lead Research Analyst",
                    )
                ],
            ),
            Ruleset(
                name="Objective",
                rules=[
                    Rule(
                        value="Discover innovative advancements in artificial intelligence and data analytics",
                    )
                ],
            ),
            Ruleset(
                name="Background",
                rules=[
                    Rule(
                        value="""You are part of a prominent technology research institute.
                        Your speciality is spotting new trends.
                        You excel at analyzing intricate data and delivering practical insights."""
                    )
                ],
            ),
            Ruleset(
                name="Desired Outcome",
                rules=[
                    Rule(
                        value="Comprehensive analysis report in list format",
                    )
                ],
            ),
        ],
    )

    return researcher


if __name__ == "__main__":
    # Set up the EventBus
    EventBus.add_event_listener(
        EventListener(
            event_listener_driver=GriptapeCloudEventListenerDriver(
                api_key=get_listener_api_key()
            )
        )
    )
    agent = build_researcher()
    agent.run(sys.argv[1])
