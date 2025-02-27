import logging

from griptape.drivers.web_scraper.trafilatura import TrafilaturaWebScraperDriver
from griptape.drivers.web_search.duck_duck_go import DuckDuckGoWebSearchDriver
from griptape.loaders import WebLoader
from griptape.rules import Rule
from griptape.structures import Agent
from griptape.tasks import PromptTask
from griptape.tools import (
    BaseTool,
    WebScraperTool,
    WebSearchTool,
)

from .griptape.read_only_conversation_memory import ReadOnlyConversationMemory

logger = logging.getLogger()


def get_tools(message: str, *, dynamic: bool = False) -> list[BaseTool]:
    """Get tools for the Agent to use. if dynamic=True, the LLM will decide what tools to use.

    based on the user input and the conversation history.
    """
    tools_dict = _init_tools_dict()
    if not dynamic:
        return [tool for tool, _ in tools_dict.values()]

    tools_descriptions = {k: description for k, (_, description) in tools_dict.items()}

    agent = Agent(
        tasks=[
            PromptTask(
                input="Given the input, what tools are needed to give an accurate response?"
                "Input: '{{ args[0] }}' Tools: {{ args[1] }}",
                rules=[
                    Rule("The tool name is the key in the tools dictionary, and the description is the value."),
                    Rule("Only respond with a comma-separated list of tool names."),
                    Rule("Do not include any other information."),
                    Rule("If no tools are needed, respond with 'None'."),
                ],
            ),
        ],
        conversation_memory=ReadOnlyConversationMemory(),
    )
    output = agent.run(message, tools_descriptions).output.value
    tool_names = output.split(",") if output != "None" else []
    logger.info("Tools needed: %s", tool_names)
    return [tools_dict[tool_name.strip()][0] for tool_name in tool_names]


def _init_tools_dict() -> dict[str, tuple[BaseTool, str]]:
    """Initialize the tools dictionary.

    The return value is a dictionary where the key is the tool name
    and the value is a tuple containing the Tool object and a description
    of what the tool can do.
    """
    tools_dict: dict = {
        "web_scraper": (
            WebScraperTool(
                web_loader=WebLoader(web_scraper_driver=TrafilaturaWebScraperDriver()),
            ),
            "Can be used find information on a web page. Should be used with web_search.",
        ),
        "web_search": (
            WebSearchTool(
                web_search_driver=DuckDuckGoWebSearchDriver(),
            ),
            "Can be used to search the web for information. Should be used with web_scraper.",
        ),
    }

    return tools_dict
