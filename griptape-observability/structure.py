import os
import argparse
from dotenv import load_dotenv

from griptape.drivers import GriptapeCloudEventListenerDriver, GriptapeCloudObservabilityDriver
from griptape.events import EventListener, EventBus
from griptape.observability import Observability
from griptape.structures import Agent


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if not api_key:
        print(
            """
            ****WARNING****: No value was found for the 'GT_CLOUD_API_KEY' environment variable.
            This environment variable is required for the GriptapeCloudObservabilityDriver.
            You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/keys .
            Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
            """
        )
        raise ValueError("Missing GT_CLOUD_API_KEY environment variable.")
    return api_key

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prompt",
        default="What is the air speed velocity of an unladen swallow?",
        help="Specify this to prompt the Griptape agent",
    )

    args = parser.parse_args()
    prompt = args.prompt

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
        raise EnvironmentError("This script must be run in a Griptape Cloud or Skatepark emulator environment.")

    observability_driver = GriptapeCloudObservabilityDriver(api_key=get_listener_api_key(), structure_run_id=os.environ["GT_CLOUD_STRUCTURE_RUN_ID"])

    with Observability(observability_driver=observability_driver):
        agent = Agent().run(prompt)
