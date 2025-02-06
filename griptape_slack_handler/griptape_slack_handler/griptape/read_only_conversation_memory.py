from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define

from griptape.memory.structure import ConversationMemory

if TYPE_CHECKING:
    from griptape.memory.structure import BaseConversationMemory, Run


@define
class ReadOnlyConversationMemory(ConversationMemory):
    """
    Read-only conversation memory for providing context to the LLM without adding its own.
    """

    def add_run(self, run: Run) -> BaseConversationMemory:
        return self
