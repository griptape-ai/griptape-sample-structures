import os
import sys

from dotenv import load_dotenv
from griptape.drivers import GoogleWebSearchDriver
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.tools import (
    PromptSummaryTool,
    WebScraperTool,
    WebSearchTool,
)
from griptape.utils import GriptapeCloudStructure

load_dotenv()


def build_researcher() -> Agent:
    """Build a Researcher Structure."""
    return Agent(
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


if __name__ == "__main__":
    with GriptapeCloudStructure():
        agent = build_researcher()
        agent.run(sys.argv[1])
