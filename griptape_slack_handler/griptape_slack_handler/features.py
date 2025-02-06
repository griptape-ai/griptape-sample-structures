import os


def persist_thoughts_enabled() -> bool:
    """
    Whether the Slack Bot will overwrite its thought process with the final output.
    Defaults to False
    """
    return get_feature("PERSIST_THOUGHTS", False)


def stream_output_enabled() -> bool:
    """
    Whether the response will be streamed. Defaults to False
    """
    return get_feature("STREAM_OUTPUT", False)


def dynamic_tools_enabled() -> bool:
    """
    Whether the LLM will dynamically choose Tools. Defaults to False.
    """
    return get_feature("DYNAMIC_TOOLS", False)


def dynamic_rulesets_enabled() -> bool:
    """
    Whether the Agent will have dynamic rulesets based on the incoming user/channel/team/etc ids. Defaults to True
    """
    return get_feature("DYNAMIC_RULESETS", True)


def thread_history_enabled() -> bool:
    """
    Whether the Slack App will persist any thread in any channel that it is in, and use the thread for response context.
    Defaults to True
    """
    return get_feature("THREAD_HISTORY", True)


def get_feature(feature: str, default: bool) -> bool:
    """
    Gets a feature from the environment.
    """
    default_str = "true" if default else "false"
    return os.getenv(f"FEATURE_{feature}", default_str).lower() == "true"
