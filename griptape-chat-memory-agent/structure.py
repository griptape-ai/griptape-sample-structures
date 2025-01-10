import os
from typing import Optional
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.configs import Defaults
from griptape.drivers import (
    GriptapeCloudConversationMemoryDriver,
)
from griptape.drivers import (
    GriptapeCloudEventListenerDriver,
    GriptapeCloudRulesetDriver,
    GriptapeCloudVectorStoreDriver
)
from griptape.events import EventListener, EventBus
from griptape.rules.ruleset import Ruleset
from griptape.tools import BaseTool, RagTool
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import (
    PromptResponseRagModule,
    VectorStoreRetrievalRagModule,
)
from griptape.engines.rag.stages import ResponseRagStage, RetrievalRagStage
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


def get_knowledge_base_tools(knowledge_base_id: Optional[str]) -> list[BaseTool]:
    if knowledge_base_id is None:
        return []
    else:
        engine = RagEngine(
        retrieval_stage=RetrievalRagStage(
            retrieval_modules=[
                VectorStoreRetrievalRagModule(
                    vector_store_driver=GriptapeCloudVectorStoreDriver(
                        api_key=get_listener_api_key(),
                        knowledge_base_id=knowledge_base_id,
                    )
                )
            ]
        ),
        response_stage=ResponseRagStage(
            response_modules=[PromptResponseRagModule()],
        ),
    )
        return [
            RagTool(
            description="Contains information about the company and its operations",
            rag_engine=engine,
        ),
        ]


def get_rulesets(ruleset_alias: Optional[str]) -> list[Ruleset]:
    if ruleset_alias is None:
        return []
    else:
        return [
            Ruleset(
                name=ruleset_alias,
                ruleset_driver=GriptapeCloudRulesetDriver(
                    api_key=get_listener_api_key(),
                    base_url=get_base_url(),
                ),
            )
        ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-k",
        "--knowledge-base-id",
        default=None,
        help="Set the Griptape Cloud Knowledge Base ID you wish to use",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        default="Hello there!",
        help="The prompt you wish to use",
    )
    parser.add_argument(
        "-r",
        "--ruleset-alias",
        default=None,
        help="Set the Griptape Cloud Ruleset alias to use",
    )
    parser.add_argument(
        "-s",
        "--stream",
        default=False,
        action="store_true",
        help="Enable streaming mode for the Agent",
    )
    parser.add_argument(
        "-t",
        "--thread_id",
        default=None,
        help="Set the Griptape Cloud Thread ID you wish to use",
    )

    args = parser.parse_args()
    knowledge_base_id = args.knowledge_base_id
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
                    event_listener_driver=event_driver,
                ),
            ]
        )
    else:
        load_dotenv()

    Defaults.drivers_config.conversation_memory_driver = (
        GriptapeCloudConversationMemoryDriver(
            api_key=get_listener_api_key(),
            thread_id=thread_id,
        )
    )

    agent = Agent(
        rulesets=get_rulesets(ruleset_alias),
        tools=get_knowledge_base_tools(knowledge_base_id),
        stream=stream,
    )

    result = agent.run(prompt)
