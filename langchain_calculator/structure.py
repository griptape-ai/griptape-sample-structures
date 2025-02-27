from dotenv import load_dotenv
from griptape.artifacts import TextArtifact
from griptape.utils import GriptapeCloudStructure
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


with GriptapeCloudStructure() as structure:
    structure.output = TextArtifact(value=TextArtifact(result))
