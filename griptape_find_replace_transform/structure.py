import argparse
import os
import re
from griptape.events import EventBus, EventListener, FinishStructureRunEvent
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.artifacts import TextArtifact

from dotenv import load_dotenv


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def replace_substrings_case_insensitive(input_string, find_string, replace_string):
    pattern = re.compile(re.escape(find_string), re.IGNORECASE)
    return pattern.sub(replace_string, input_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_artifacts")  # positional
    parser.add_argument(
        "-f",
        "--find_word",
        help="The word you wish to find in the artifacts",
    )
    parser.add_argument(
        "-r",
        "--replace_with",
        help="The word you wish to replace with",
    )

    args = parser.parse_args()

    load_dotenv()

    result = replace_substrings_case_insensitive(
        args.input_artifacts, args.find_word, args.replace_with
    )

    print(result)

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver()

        task_input = TextArtifact(value=None)
        done_event = FinishStructureRunEvent(
            output_task_input=task_input, output_task_output=TextArtifact(value=result)
        )

        EventBus.add_event_listener(EventListener(event_listener_driver=event_driver))
        EventBus.publish_event(done_event, flush=True)
        print("Published final event")
