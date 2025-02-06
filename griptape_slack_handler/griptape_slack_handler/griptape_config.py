from typing import Optional

from griptape.configs import Defaults
from griptape.drivers import (
    GriptapeCloudConversationMemoryDriver,
    GriptapeCloudRulesetDriver,
)


def load_griptape_config() -> None:
    """Load the Default Griptape configuration."""

    Defaults.drivers_config.ruleset_driver = GriptapeCloudRulesetDriver(
        raise_not_found=False
    )
    Defaults.drivers_config.conversation_memory_driver = (
        GriptapeCloudConversationMemoryDriver()
    )


def set_thread_alias(thread_alias: Optional[str]) -> None:
    """Set the thread alias for the conversation memory driver."""
    Defaults.drivers_config.conversation_memory_driver.alias = thread_alias
