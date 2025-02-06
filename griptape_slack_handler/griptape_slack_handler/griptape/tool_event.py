from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from griptape.events import BaseEvent

if TYPE_CHECKING:
    from griptape.tools import BaseTool


@define(kw_only=True)
class ToolEvent(BaseEvent):
    """An event that contains Tools.

    Attributes:
        tools: The tools to use for the event.
        stream: Whether the Prompt Driver is streaming.
    """

    tools: list[BaseTool] = field()
    stream: bool = field(default=False)
