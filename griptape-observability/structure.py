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
    api_key = os.environ.get("GT_CLOUD_API_KEY", "gt-2rHdtJHIh99puMw7TPPfzC3c32ER3JpcHRhcGU=taCkUfT4USMy3dFtT09iUi9U0eo")
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
        load_dotenv()
        event_driver = None

    observability_driver = GriptapeCloudObservabilityDriver(api_key=get_listener_api_key(), structure_run_id="69d64d34-2b2f-4ba1-94ee-560403cce65b")

    with Observability(observability_driver=observability_driver):
        agent = Agent().run(prompt)
