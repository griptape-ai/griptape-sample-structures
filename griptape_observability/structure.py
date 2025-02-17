import argparse
import os

from griptape.drivers import (
    GriptapeCloudEventListenerDriver,
    GriptapeCloudObservabilityDriver,
)
from griptape.events import EventBus, EventListener
from griptape.observability import Observability
from griptape.structures import Agent


def get_structure_run_id() -> str:
    structure_run_id = os.environ.get("GT_CLOUD_STRUCTURE_RUN_ID", "")
    if not structure_run_id:
        msg = "This script must be run in a Griptape Cloud or Skatepark emulator environment."
        raise OSError(msg)
    return structure_run_id


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if not api_key:
        msg = "Missing GT_CLOUD_API_KEY environment variable."
        raise ValueError(msg)
    return api_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prompt",
        default="What is the air speed velocity of an unladen swallow?",
        help="Specify this to run the Griptape agent with a custom prompt",
    )

    args = parser.parse_args()
    prompt = args.prompt

    structure_run_id = get_structure_run_id()
    api_key = get_listener_api_key()

    event_driver = GriptapeCloudEventListenerDriver(api_key=api_key)
    EventBus.add_event_listeners(
        [
            EventListener(
                # By default, GriptapeCloudEventListenerDriver uses the api key provided
                # in the GT_CLOUD_API_KEY environment variable.
                event_listener_driver=event_driver,
            ),
        ]
    )

    observability_driver = GriptapeCloudObservabilityDriver(
        api_key=get_listener_api_key(), structure_run_id=structure_run_id
    )
    with Observability(observability_driver=observability_driver):
        agent = Agent().run(prompt)
