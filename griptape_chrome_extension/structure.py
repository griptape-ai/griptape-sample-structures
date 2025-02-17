from griptape.structures import Agent
from griptape.utils import GriptapeCloudStructure
from griptape.drivers.memory.conversation.griptape_cloud_conversation_memory_driver import (
    GriptapeCloudConversationMemoryDriver,
)
from griptape.tools import CalculatorTool, PromptSummaryTool
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver
from griptape.memory.structure import ConversationMemory
import os
import sys

input = sys.argv[1]

# `GriptapeCloud` will configure the EventBus with `GriptapeCloudEventListenerDriver`
with GriptapeCloudStructure():
    cloud_conversation_driver = GriptapeCloudConversationMemoryDriver(
        api_key=os.environ["GT_CLOUD_API_KEY"],
        alias="griptape_browser_extension_thread",
    )
    structure = Agent(
        prompt_driver=OpenAiChatPromptDriver(model="gpt-4o-mini", stream=True),
        tools=[CalculatorTool(off_prompt=False), PromptSummaryTool(off_prompt=True)],
        conversation_memory=ConversationMemory(
            conversation_memory_driver=cloud_conversation_driver
        ),
    )
    structure.run(input)
