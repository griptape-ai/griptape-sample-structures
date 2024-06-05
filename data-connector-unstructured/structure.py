import boto3
import os
import sys

from unstructured_client import UnstructuredClient
from unstructured_client.models import shared

from dotenv import load_dotenv

from griptape.artifacts import ListArtifact, TextArtifact
from griptape.drivers import (
    GriptapeCloudEventListenerDriver,
)
from griptape.artifacts import TextArtifact
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventListener
from griptape.structures import Workflow
from griptape.tasks import CodeExecutionTask



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

s3_uri = sys.argv[1]

if is_running_in_managed_environment():
    event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
else:
    load_dotenv()
    event_driver = None

workflow = Workflow(event_listeners=[EventListener(driver=event_driver)],)

def test_fn(task: CodeExecutionTask) -> TextArtifact:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    s3_uri = sys.argv[1]
    bucket, key = s3_uri.split('/',2)[-1].split('/',1)
    print(f"Bucket: {bucket} Key: {key}")

    s3_client.download_file(bucket, key, key)

    # Update here with your api key and server url
    client = UnstructuredClient(
        api_key_auth=os.environ.get('UNSTRUCTURED_API_KEY'),
        server_url=os.environ.get('UNSTRUCTURED_SERVER_URL'),
    )

    with open(key, "rb") as f:
        files=shared.Files(
            content=f.read(),
            file_name=key,
        )

    # You can choose fast, hi_res or ocr_only for strategy, learn more in the docs at step 4
    req = shared.PartitionParameters(files=files, strategy="auto")

    resp = client.general.partition(req)
    artifacts = []
    for element in resp.elements:
        artifacts.append(TextArtifact(value=element["text"]))
    return ListArtifact(artifacts)

summary_task = CodeExecutionTask(
    run_fn=test_fn
)

workflow.add_task(summary_task)

result = workflow.run()
