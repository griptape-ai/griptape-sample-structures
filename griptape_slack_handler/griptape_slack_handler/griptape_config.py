from griptape.configs import Defaults
from griptape.drivers.memory.conversation.griptape_cloud import GriptapeCloudConversationMemoryDriver
from griptape.drivers.ruleset.griptape_cloud import GriptapeCloudRulesetDriver


def load_griptape_config() -> None:
    """Load the Default Griptape configuration."""
    Defaults.drivers_config.ruleset_driver = GriptapeCloudRulesetDriver(raise_not_found=False)
    Defaults.drivers_config.conversation_memory_driver = GriptapeCloudConversationMemoryDriver()


def set_thread_alias(thread_alias: str | None) -> None:
    """Set the thread alias for the conversation memory driver."""
    Defaults.drivers_config.conversation_memory_driver.alias = thread_alias
