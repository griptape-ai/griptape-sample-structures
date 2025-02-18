import sys

from dotenv import load_dotenv
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.utils import GriptapeCloudStructure

load_dotenv()


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
    with GriptapeCloudStructure():
        agent = build_writer(sys.argv[1], sys.argv[2], sys.argv[3])
        agent.run(sys.argv[4])
