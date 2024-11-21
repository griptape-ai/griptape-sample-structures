from __future__ import annotations

from typing import Optional

import logging
import json

from griptape.events import (
    BaseEvent,
    EventListener,
    StartStructureRunEvent,
    StartActionsSubtaskEvent,
    FinishActionsSubtaskEvent,
    ActionChunkEvent,
    TextChunkEvent,
)

from .griptape.tool_event import ToolEvent
from .griptape.slack_event_listener_driver import SlackEventListenerDriver
from .slack_util import thought_block, action_block, emoji_block

logger = logging.getLogger()


def event_listeners(*, stream: bool, **kwargs) -> list[EventListener]:
    # if stream is True, we will use the batched driver to deliver chunk events
    # and continuously update the slack message
    if stream:
        stream_driver = SlackEventListenerDriver(**kwargs, batched=True, batch_size=100)
        return [
            EventListener(
                handler,
                event_types=[
                    ToolEvent,
                    TextChunkEvent,
                    ActionChunkEvent,
                ],
                event_listener_driver=stream_driver,
            )
        ]

    # WIP: use event listeners to create different UXs of different actions the LLM is taking
    driver = SlackEventListenerDriver(**kwargs)
    return [
        EventListener(
            handler,
            event_types=[
                ToolEvent,
                StartStructureRunEvent,
                StartActionsSubtaskEvent,
                FinishActionsSubtaskEvent,
            ],
            event_listener_driver=driver,
        )
    ]


def handler(event: BaseEvent) -> Optional[dict]:
    if isinstance(event, ToolEvent):
        return tool_event_handler(event)
    if isinstance(event, StartStructureRunEvent):
        return start_structure_handler(event)
    if isinstance(event, StartActionsSubtaskEvent):
        return start_actions_subtask_handler(event)
    if isinstance(event, FinishActionsSubtaskEvent):
        return finish_actions_subtask_handler(event)
    if isinstance(event, TextChunkEvent):
        return text_stream_handler(event)
    if isinstance(event, ActionChunkEvent):
        return action_stream_handler(event)
    return None


def tool_event_handler(event: ToolEvent) -> Optional[dict]:
    if not event.tools:
        return None

    if event.stream:
        return {
            "text": f"Tools needed: {', '.join([tool.name for tool in event.tools])}\n\n",
        }
    else:
        return {
            "text": "Tools",
            "blocks": [action_block(f"I need the {tool.name}") for tool in event.tools],
        }


def start_structure_handler(event: StartStructureRunEvent) -> Optional[dict]:
    return {
        "text": "Starting...",
        "blocks": [emoji_block(":envelope:", "Reading the data...")],
    }


def start_actions_subtask_handler(event: StartActionsSubtaskEvent) -> Optional[dict]:
    if event.subtask_actions is None:
        return None
    blocks = []
    if event.subtask_thought is not None:
        blocks.append(thought_block(event.subtask_thought))
    for action in event.subtask_actions:
        action_input = "\n".join(
            [f"*{key}*: _{value}_ " for key, value in action["input"]["values"].items()]
        )
        blocks.append(
            action_block(
                f"_I will use {action['name']}.{action['path']} with input:_\n\n{action_input}",
                format=False,
            )
        )

    return {"blocks": blocks, "text": "Thought..."}


def finish_actions_subtask_handler(event: FinishActionsSubtaskEvent) -> Optional[dict]:
    return {
        "text": "Finishing...",
        "blocks": [emoji_block(":pencil:", "Analyzing the data...")],
    }


def text_stream_handler(event: TextChunkEvent) -> Optional[dict]:
    if not event.token:
        return None

    return {
        "text": event.token,
    }


def action_stream_handler(event: ActionChunkEvent) -> Optional[dict]:
    action = event.partial_input
    if action is not None:
        try:
            loaded = json.loads(action)
            action = f"I need the {event.name} with action {event.path} with input: {json.dumps(loaded['values'], indent=2)}"
        except Exception:
            pass

        return {
            "text": action,
        }

    return None
