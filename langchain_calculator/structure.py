import os

from dotenv import load_dotenv
from griptape.artifacts import TextArtifact
from griptape.drivers import GriptapeCloudEventListenerDriver
from griptape.events import EventBus, EventListener, FinishStructureRunEvent
from langchain_core.messages import AIMessage, ToolCall
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int


@tool
def add(first_int: int, second_int: int) -> int:
    """Add two integers."""
    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    """Exponentiate the base to the exponent power."""
    return base**exponent


def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if is_running_in_managed_environment() and not api_key:
        pass
    return api_key


llm = ChatOpenAI(model="gpt-4-turbo")
tools = [multiply, exponentiate, add]
llm_with_tools = llm.bind_tools(tools)
tool_map = {tool.name: tool for tool in tools}


def call_tools(msg: AIMessage) -> list[ToolCall]:
    """Simple sequential tool calling helper."""
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = msg.tool_calls.copy()
    for tool_call in tool_calls:
        tool_call["output"] = tool_map[tool_call["name"]].invoke(tool_call["args"])  # pyright: ignore[reportGeneralTypeIssues]
    return tool_calls


chain = llm_with_tools | call_tools

agent_input = "What's 23 times 7, and what's five times 18 and add a million plus a billion and cube thirty-seven"
result = chain.invoke(agent_input)

task_input = TextArtifact(value=agent_input)
task_output = TextArtifact(value=result)
done_event = FinishStructureRunEvent(output_task_input=task_input, output_task_output=task_output)

api_key = os.getenv("GT_CLOUD_API_KEY")


def is_running_in_managed_environment() -> bool:
    return "GT_CLOUD_STRUCTURE_RUN_ID" in os.environ


if is_running_in_managed_environment():
    event_driver = GriptapeCloudEventListenerDriver(api_key=get_listener_api_key())
    EventBus.add_event_listener(EventListener(event_listener_driver=event_driver))
    EventBus.publish_event(done_event, flush=True)
else:
    pass
