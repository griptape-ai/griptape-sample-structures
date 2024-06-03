from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.runnables import (
    Runnable,
)

from griptape.artifacts import TextArtifact
from griptape.events import FinishStructureRunEvent
from griptape.drivers import GriptapeCloudEventListenerDriver

from dotenv import load_dotenv
from urllib.parse import urljoin
import os
import requests

load_dotenv()


@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int


@tool
def add(first_int: int, second_int: int) -> int:
    "Add two integers."
    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    return base**exponent


llm = ChatOpenAI(model="gpt-4-turbo")
tools = [multiply, exponentiate, add]
llm_with_tools = llm.bind_tools(tools)
tool_map = {tool.name: tool for tool in tools}


def call_tools(msg: AIMessage) -> Runnable:
    """Simple sequential tool calling helper."""
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = msg.tool_calls.copy()
    for tool_call in tool_calls:
        tool_call["output"] = tool_map[tool_call["name"]].invoke(tool_call["args"])
    return tool_calls


chain = llm_with_tools | call_tools

input = "What's 23 times 7, and what's five times 18 and add a million plus a billion and cube thirty-seven"
result = chain.invoke(input)

print(result)

task_input = TextArtifact(value=input)
task_output = TextArtifact(value=result)
done_event = FinishStructureRunEvent(
    output_task_input=task_input, output_task_output=task_output
)

api_key = os.getenv("GT_CLOUD_API_KEY")
event_driver = GriptapeCloudEventListenerDriver(
    api_key=api_key
)

event_driver.publish_event(done_event)

structure_run_id = os.getenv("GT_CLOUD_STRUCTURE_RUN_ID")
base_url = os.getenv("GT_CLOUD_BASE_URL")
url = urljoin(base_url, f"/api/structure-runs/{structure_run_id}/events")

header_body=f"Bearer {api_key}"
headers = {"Authorization":header_body}
response = requests.post(url=url, json=done_event.to_dict(), headers=headers)
print(response)