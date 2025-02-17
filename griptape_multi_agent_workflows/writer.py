import os
import sys

from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventBus, EventListener
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if not api_key:
        pass
    return api_key


def build_writer(role: str, goal: str, backstory: str) -> Agent:
    """
    Build a Writer Structure.

    Args:
        role: The role of the writer.
        goal: The goal of the writer.
        backstory: The backstory of the writer.

    """
    return Agent(
        id=role.lower().replace(" ", "_"),
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


if __name__ == "__main__":
    # Set up the EventBus
    EventBus.add_event_listener(
        EventListener(event_listener_driver=GriptapeCloudEventListenerDriver(api_key=get_listener_api_key()))
    )
    agent = build_writer(sys.argv[1], sys.argv[2], sys.argv[3])
    agent.run(sys.argv[4])
