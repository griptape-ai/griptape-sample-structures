from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import logging
import re

from griptape.events import EventBus
from griptape.artifacts import ErrorArtifact, TextArtifact
from griptape.rules import Ruleset
from griptape.structures import Agent
from griptape.memory.structure import ConversationMemory, Run

from griptape_slack_handler.griptape_event_handlers import ToolEvent

from .griptape_tool_box import get_tools
from .griptape_config import load_griptape_config, set_thread_alias
from .features import dynamic_rulesets_enabled, dynamic_tools_enabled

if TYPE_CHECKING:
    from griptape.events import EventListener


logger = logging.getLogger()


load_griptape_config()


def try_add_to_thread(
    message: str, *, thread_alias: Optional[str] = None, user_id: str
) -> None:
    set_thread_alias(thread_alias)
    # find all the user_ids @ mentions in the message
    mentioned_user_ids = re.findall(r"<@([\w]+)>", message)
    rulesets = [Ruleset(name=mentioned_user) for mentioned_user in mentioned_user_ids]
    for ruleset in rulesets:
        # If the message is mentioning the bot, don't add it to the memory
        # because the bot will already be responding to the message,
        # and the message will be in conversation memory already
        if ruleset.meta.get("type") == "bot":
            return

    memory = ConversationMemory()
    # WIP. since messages that do not tag the bot are not being added to the cloud Thread,
    # the bot can miss context. This inserts those messages into the Thread, which
    # later can be used to provide context via ConversationMemory. this seems to work okay,
    # but it can confuse the LLM
    memory.add_run(
        Run(
            input=TextArtifact(
                f"Do not respond. Only use this message for future context. Message: 'user {user_id}: {message}'"
            ),
            output=TextArtifact(""),
        )
    )


def get_rulesets(**kwargs) -> list[Ruleset]:
    return (
        [Ruleset(name=value) for value in kwargs.values()]
        if dynamic_rulesets_enabled()
        else []
    )


def agent(
    message: str,
    *,
    thread_alias: Optional[str] = None,
    user_id: str,
    rulesets: list[Ruleset],
    event_listeners: list[EventListener],
    stream: bool,
) -> str:
    set_thread_alias(thread_alias)
    dynamic_tools = dynamic_tools_enabled() or any(
        [ruleset.meta.get("dynamic_tools", False) for ruleset in rulesets]
    )
    tools = get_tools(message, dynamic=dynamic_tools)
    EventBus.add_event_listeners(event_listeners)
    EventBus.publish_event(ToolEvent(tools=tools, stream=stream), flush=True)

    agent = Agent(
        input="user_id '<@{{ args[0] }}>': {{ args[1] }}",
        tools=tools,
        rulesets=rulesets,
        stream=stream,
    )
    output = agent.run(user_id, message).output
    if isinstance(output, ErrorArtifact):
        raise ValueError(output.to_text())
    return output.to_text()
