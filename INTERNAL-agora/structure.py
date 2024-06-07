import boto3
import os
import sys

from dotenv import load_dotenv
from typing import Optional

from griptape.artifacts import ListArtifact, TextArtifact
from griptape.loaders import CsvLoader
from griptape.drivers import (
    GriptapeCloudEventListenerDriver,
)
from griptape.events import (
    FinishStructureRunEvent,
)
from griptape.utils import load_file



def is_running_in_managed_environment() -> bool:
    """Determine if the program is running in a managed environment (e.g., Griptape Cloud or Skatepark emulator).

    Returns:
        bool: True if the program is running in a managed environment, False otherwise.
    """
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_listener_api_key() -> str:
    """The event driver expects a Griptape Cloud API Key as a parameter.
    When your program is running in Griptape Cloud, you will need to provide a
    valid Griptape Cloud API Key in the GT_CLOUD_API_KEY environment variable, otherwise
    the service will not authorize the necessary calls.
    You can create an API Key by visiting https://cloud.griptape.ai/keys
    When running in Skatepark, the API key is not needed since it isn't validating calls.

    Returns:
        The Griptape Cloud API Key to authorize calls.
    """
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


def generate_text_artifacts(s3_uri, event_driver: Optional[GriptapeCloudEventListenerDriver]) -> list[TextArtifact]:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    bucket, key = s3_uri.split('/',2)[-1].split('/',1)

    print(f"Bucket: {bucket} Key: {key}")

    s3_client.download_file(bucket, key, key)

    loader = CsvLoader()

    csv_row_artifacts = loader.load(load_file(key))

    for csv_row_artifact in csv_row_artifacts:
        video_url_column_name = "Showreel"
        video_urls_string = csv_row_artifact.value[video_url_column_name]
        if video_urls_string:
            video_urls = video_urls_string.split(",")
            for video_url in video_urls:
                print(f"Showreel URL: {video_url.strip()}")
                # TODO: Call Collin's structure(s)
                video_description = "Llamas with Hats"
                csv_row_artifact.value["Showreel Description"] = video_description
        print(csv_row_artifact)

    task_input = TextArtifact(value=None)
    done_event = FinishStructureRunEvent(
        output_task_input=task_input, output_task_output=ListArtifact(csv_row_artifacts)
    )

    if event_driver:
        event_driver.publish_event(done_event, flush=True)

s3_uri = sys.argv[1]

if is_running_in_managed_environment():
    event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
else:
    load_dotenv()
    event_driver = None

generate_text_artifacts(s3_uri, event_driver)
