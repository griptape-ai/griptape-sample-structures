import argparse

from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.drivers import (
    GriptapeCloudConversationMemoryDriver,
    GriptapeCloudRulesetDriver,
    GriptapeCloudVectorStoreDriver,
)
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import (
    PromptResponseRagModule,
    VectorStoreRetrievalRagModule,
)
from griptape.engines.rag.stages import ResponseRagStage, RetrievalRagStage
from griptape.rules.ruleset import Ruleset
from griptape.structures import Agent
from griptape.tools import BaseTool, RagTool
from griptape.utils import GriptapeCloudStructure

load_dotenv()


def get_knowledge_base_tools(knowledge_base_id: str | None) -> list[BaseTool]:
    if knowledge_base_id is None:
        return []
    engine = RagEngine(
        retrieval_stage=RetrievalRagStage(
            retrieval_modules=[
                VectorStoreRetrievalRagModule(
                    vector_store_driver=GriptapeCloudVectorStoreDriver(
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


def get_rulesets(ruleset_alias: str | None) -> list[Ruleset]:
    if ruleset_alias is None:
        return []
    return [Ruleset(name=ruleset_alias, ruleset_driver=GriptapeCloudRulesetDriver())]


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

    Defaults.drivers_config.conversation_memory_driver = GriptapeCloudConversationMemoryDriver(
        thread_id=thread_id,
    )

    agent = Agent(
        rulesets=get_rulesets(ruleset_alias),
        tools=get_knowledge_base_tools(knowledge_base_id),
        stream=stream,
    )

    with GriptapeCloudStructure():
        agent.run(prompt)
