import os
import sys

from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.tools import (
    TaskMemoryClient,
    WebScraper,
    WebSearch,
)

def build_researcher():
    """Builds a Researcher Structure."""
    researcher = Agent(
        id="researcher",
        tools=[
            WebSearch(
                google_api_key=os.environ["GOOGLE_API_KEY"],
                google_api_search_id=os.environ["GOOGLE_API_SEARCH_ID"],
            ),
            WebScraper(
                off_prompt=True,
            ),
            TaskMemoryClient(off_prompt=False),
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
    agent = build_researcher()
    agent.run(sys.argv[1])
