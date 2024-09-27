import os
from typing import Optional
import requests
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.configs import Defaults
from griptape.drivers import (
    GriptapeCloudConversationMemoryDriver,
)
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener, EventBus
from griptape.rules.rule import Rule
from griptape.rules.ruleset import Ruleset
import argparse


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_base_url() -> str:
    return os.environ.get("GT_CLOUD_BASE_URL", "https://cloud.griptape.ai")


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


def get_headers():
    return {
        "Authorization": f"Bearer {get_listener_api_key()}",
        "Content-Type": "application/json",
    }


def get_rule_by_id(rule_id: str) -> dict:
    url = f"{get_base_url()}/api/rules/{rule_id}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def get_ruleset_by_alias(alias: str) -> dict:
    url = f"{get_base_url()}/api/rulesets"
    response = requests.get(url, headers=get_headers(), params={"alias": alias})
    response.raise_for_status()
    response_json = response.json()
    if not response_json["rulesets"]:
        raise ValueError(f"No ruleset found with alias '{alias}'")
    return response_json["rulesets"][0]


def get_rulesets(ruleset_alias: Optional[str]) -> list[Ruleset]:
    if ruleset_alias is None:
        return []

    ruleset = get_ruleset_by_alias(ruleset_alias)
    rule_ids = ruleset["rule_ids"]
    rules = [get_rule_by_id(rule_id) for rule_id in rule_ids]
    griptape_rulesets: list[Ruleset] = []
    rules_values = []
    for rule in rules:
        rules_values.append(Rule(rule["rule"]))
    griptape_rulesets.append(Ruleset(name=ruleset["name"], rules=rules_values))

    return griptape_rulesets


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prompt",
        default="Hello there!",
        help="The prompt you wish to use",
    )
    parser.add_argument(
        "-t",
        "--thread_id",
        default=None,
        help="The Griptape Cloud Thread ID you wish to use",
    )
    parser.add_argument(
        "-r",
        "--ruleset-alias",
        default=None,
        help="Set the ruleset alias to use",
    )
    parser.add_argument(
        "-s",
        "--stream",
        default=False,
        action="store_true",
        help="Enable streaming mode for the Agent",
    )

    args = parser.parse_args()
    prompt = args.prompt
    thread_id = args.thread_id
    ruleset_alias = args.ruleset_alias
    stream = args.stream

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
        EventBus.add_event_listeners(
            [
                EventListener(
                    # By default, GriptapeCloudEventListenerDriver uses the api key provided
                    # in the GT_CLOUD_API_KEY environment variable.
                    driver=event_driver,
                ),
            ]
        )
    else:
        load_dotenv()
        event_driver = None

    Defaults.drivers_config.conversation_memory_driver = (
        GriptapeCloudConversationMemoryDriver(
            api_key=get_listener_api_key(),
            thread_id=thread_id,
        )
    )

    agent = Agent(rulesets=get_rulesets(ruleset_alias), stream=stream)

    result = agent.run(prompt)
