from __future__ import annotations

import argparse
import csv
import json
import logging
import os
from io import BytesIO
from pathlib import Path

import pypdf
from attrs import define
from dotenv import load_dotenv
from griptape.artifacts import ListArtifact, TextArtifact
from griptape.drivers import (
    GriptapeCloudEventListenerDriver,
    GriptapeCloudFileManagerDriver,
)
from griptape.events import EventBus, EventListener, FinishStructureRunEvent
from griptape.loaders import PdfLoader
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent

logger = logging.getLogger(__name__)


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


def get_gtc_base_url() -> str:
    return os.environ.get("GT_CLOUD_BASE_URL", "https://cloud.griptape.ai")


def get_gtc_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if is_running_in_managed_environment() and not api_key:
        msg = "No value was found for the 'GT_CLOUD_API_KEY' environment variable."
        raise ValueError(msg)
    return api_key


csv_rules = Ruleset(
    name="csv",
    rules=[
        Rule("You reformat input text"),
        Rule("Do not add any additional information to the output"),
        Rule("Your output is used programmatically, so it should be in a machine-readable format"),
        Rule("A JSON list starts with '[' and ends with ']'"),
        Rule("Remove any superfluous whitespace"),
    ],
)

agent = Agent(conversation_memory=None, rulesets=[csv_rules])


@define
class AWSBillPdfLoader(PdfLoader):
    region = "UNKNOWN"
    service = "UNKNOWN"
    type = "UNKNOWN"

    def parse(
        self,
        data: bytes,
    ) -> ListArtifact:
        reader = pypdf.PdfReader(BytesIO(data), strict=True)
        artifacts = []
        for page in reader.pages:
            extracted_text = page.extract_text(extraction_mode="layout")
            artifacts.extend(self._text_to_artifacts(extracted_text))
        return ListArtifact(artifacts)

    def _text_to_artifacts(self, text: str) -> list[TextArtifact]:  # noqa: C901, PLR0912
        artifacts = []

        chunks = text.splitlines()

        for chunk in chunks:
            lstrip_chunk = chunk.lstrip()
            spaces = len(chunk) - len(lstrip_chunk)
            if "USD" in lstrip_chunk:
                if 11 <= spaces <= 14:  # noqa: PLR2004
                    striped_value = lstrip_chunk.split("USD")[0].strip()
                    # Special case for CodeBuild USW2-Build-Min:ARM:g1.small like types
                    if striped_value.startswith(("AWS", "Amazon", "CodeBuild ")):
                        self.type = striped_value
                    else:
                        response = agent.run(
                            'Only return a single word, GEOGRAPHIC or OTHER. "Any" must be classified as GEOGRAPHIC. '
                            "Phrases that are related to geography or locations on Earth must be classified at GEOGRAPHIC."  # noqa: E501
                            'Classify the following phrase after removing superfluous whitespace from it: "{striped_value}"'  # noqa: E501
                        )
                        if "GEOGRAPHIC" in response.output.value:
                            self.region = striped_value
                        elif "OTHER" in response.output.value:
                            self.service = striped_value
                        else:
                            logger.warning("Unrecognized type: %s", striped_value)
                            continue
                elif 16 <= spaces <= 18:  # noqa: PLR2004
                    if "(USD" in lstrip_chunk:
                        usd_split = lstrip_chunk.rsplit("(USD", 1)
                    elif "USD" in lstrip_chunk:
                        usd_split = lstrip_chunk.rsplit("USD", 1)
                    else:
                        logger.warning("Unrecognized USD format: %s", lstrip_chunk)
                        continue

                    cost = usd_split[1]
                    try:
                        float(cost)
                    except ValueError:
                        logger.warning("Unrecognized cost: %s", cost)
                        continue

                    usage_split = usd_split[0].rsplit("    ")
                    usage = list(filter(None, usage_split))[-1].strip()
                    quantity_and_unit = usage.split(" ", 1)
                    quantity = quantity_and_unit[0]
                    try:
                        unit = quantity_and_unit[1]
                    except IndexError:
                        unit = ""

                    description = next(filter(None, usage_split)).strip()
                    result = f'["{self.region}", "{self.service}", "{self.type}", "{quantity}", "{unit}", "{cost}", "{description}"]'  # noqa: E501
                    formatted_value = agent.run(
                        f"Reformat, remove whitespace that is inside of words, and return the following: {result}"
                    ).output.value

                    artifacts.append(TextArtifact(formatted_value))
                else:
                    logger.warning("Unrecognized spaces: %s", spaces)
                    continue

        return artifacts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bucket_id",
        default=None,
        help="The Griptape Cloud Bucket source of PDF Asset and destination of CSV Asset.",
    )
    parser.add_argument(
        "-d",
        "--workdir",
        default="",
        help="The working directory location of PDF and CSV in the Griptape Cloud Bucket.",
    )
    parser.add_argument(
        "-p",
        "--pdf_file_name",
        default=None,
        help="The Griptape Cloud Asset file name for the input PDF.",
    )
    parser.add_argument(
        "-c",
        "--csv_file_name",
        default=None,
        help="The Griptape Cloud Asset file name for the output CSV.",
    )

    args = parser.parse_args()
    bucket_id = args.bucket_id
    workdir = args.workdir
    pdf_file_name = args.pdf_file_name
    csv_file_name = args.csv_file_name

    if is_running_in_managed_environment():
        event_driver = GriptapeCloudEventListenerDriver(api_key=get_gtc_api_key(), base_url=get_gtc_base_url())
        EventBus.add_event_listeners(
            [
                EventListener(
                    # By default, GriptapeCloudEventListenerDriver uses the api key provided
                    # in the GT_CLOUD_API_KEY environment variable.
                    event_listener_driver=event_driver,
                ),
            ]
        )
    else:
        load_dotenv()
        event_driver = None

    gtc_file_manager_driver = GriptapeCloudFileManagerDriver(
        api_key=get_gtc_api_key(),
        base_url=get_gtc_base_url(),
        bucket_id=bucket_id,
        workdir=workdir,
    )

    loader = AWSBillPdfLoader(file_manager_driver=gtc_file_manager_driver)
    list_artifact = loader.load(pdf_file_name)

    with open(csv_file_name, "w", newline="") as destination_file:
        fieldnames = [
            "region",
            "service",
            "type",
            "quantity",
            "unit",
            "cost",
            "description",
        ]
        writer = csv.DictWriter(destination_file, fieldnames=fieldnames)

        writer.writeheader()
        for artifact in list_artifact.value:
            writer.writerow(dict(zip(fieldnames, json.loads(artifact.value), strict=False)))

    gtc_file_manager_driver.try_save_file(path=csv_file_name, value=Path(csv_file_name).read_bytes())

    if is_running_in_managed_environment() and Path(csv_file_name).exists():
        Path(csv_file_name).unlink()

    # This code is if you run this Structure as a GTC DC
    if event_driver is not None:
        task_input = TextArtifact(value=None)
        done_event = FinishStructureRunEvent(output_task_input=task_input, output_task_output=list_artifact)

        EventBus.add_event_listener(EventListener(event_listener_driver=event_driver))
        EventBus.publish_event(done_event, flush=True)
