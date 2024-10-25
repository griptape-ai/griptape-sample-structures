import os
import argparse

from griptape.artifacts import TextArtifact, ListArtifact
from griptape.drivers import (
    GriptapeCloudEventListenerDriver,
)
from griptape.events import EventBus, EventListener, FinishStructureRunEvent
from ruleset_synchronizer import RulesetSynchronizer


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_artifacts")  # positional

    parser.add_argument(
        "-a",
        "--alias",
        help="The alias of the Ruleset to sync",
    )
    args = parser.parse_args()

    event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
    ruleset_synchronizer = RulesetSynchronizer(
        input_artifacts=args.input_artifacts, ruleset_alias=args.alias
    )
    ruleset_synchronizer.sync_ruleset()

    # This code is if you run this Structure as a GTC DC
    if event_driver is not None:
        print("Publishing final event...")

        task_input = TextArtifact(value=None)
        output = [
            TextArtifact(artifact) for artifact in args.input_artifacts.split("\n")
        ]
        done_event = FinishStructureRunEvent(
            output_task_input=task_input, output_task_output=ListArtifact(value=output)
        )

        EventBus.add_event_listener(EventListener(driver=event_driver))
        EventBus.publish_event(done_event, flush=True)
        print("Published final event")
