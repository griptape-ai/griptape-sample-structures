import os
import sys

from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener, FinishStructureRunEvent
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent

def build_writer(role: str, goal: str, backstory: str):
    """Builds a Writer Structure.

    Args:
        role: The role of the writer.
        goal: The goal of the writer.
        backstory: The backstory of the writer.
    """
    writer = Agent(
        id=role.lower().replace(" ", "_"),
        event_listeners=[
            EventListener(
                event_types=[FinishStructureRunEvent],
                driver=GriptapeCloudEventListenerDriver(
                    api_key=os.environ["GT_CLOUD_API_KEY"],
                ),
            )
        ],
        rulesets=[
            Ruleset(
                name="Position",
                rules=[
                    Rule(
                        value=role,
                    )
                ],
            ),
            Ruleset(
                name="Objective",
                rules=[
                    Rule(
                        value=goal,
                    )
                ],
            ),
            Ruleset(
                name="Backstory",
                rules=[Rule(value=backstory)],
            ),
            Ruleset(
                name="Desired Outcome",
                rules=[
                    Rule(
                        value="Full blog post of at least 4 paragraphs",
                    )
                ],
            ),
        ],
    )

    return writer

if __name__ == "__main__":
    agent = build_writer(sys.argv[1], sys.argv[2], sys.argv[3])
    agent.run(sys.argv[4])