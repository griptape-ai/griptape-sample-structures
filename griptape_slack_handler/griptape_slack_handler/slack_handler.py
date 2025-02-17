import logging
import os

from slack_bolt import App, BoltRequest, Say
from slack_sdk import WebClient

from .features import (
    persist_thoughts_enabled,
    stream_output_enabled,
    thread_history_enabled,
)
from .griptape_event_handlers import event_listeners
from .griptape_handler import agent, get_rulesets, try_add_to_thread
from .slack_util import (
    error_payload,
    markdown_blocks_list,
    thinking_payload,
)

logger = logging.getLogger()

app: App = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    logger=logger,
    process_before_response=True,  # required
)

### Slack Event Handlers ###


@app.event("message")
def message(body: dict, payload: dict, say: Say, client: WebClient) -> None:
    # only respond to direct messages, otherwise the bot
    # will respond to every message in every channel it is in
    if payload.get("channel_type") == "im":
        respond_in_thread(body, payload, say, client)
    elif payload.get("subtype") != "bot_message" and thread_history_enabled():
        # add the message to the cloud thread
        # so the bot can use it for context when
        # responding to future messages in a thread
        try_add_to_thread(
            payload["text"],
            thread_alias=payload.get("thread_ts", payload["ts"]),
            user_id=payload["user"],
        )


@app.event("app_mention")
def app_mention(body: dict, payload: dict, say: Say, client: WebClient) -> None:
    respond_in_thread(body, payload, say, client)


def should_respond_for_channel(payload: dict) -> bool:
    channel = payload.get("channel")
    channel_type = payload.get("channel_type")

    def get_channels_from_env(env_var: str) -> list:
        return os.environ[env_var].split(",") if env_var in os.environ and os.environ[env_var] != "" else []

    filter_in = get_channels_from_env("FILTER_IN_CHANNELS")
    filter_out = get_channels_from_env("FILTER_OUT_CHANNELS")
    disable_im = os.environ.get("DISABLE_IM", "false").lower() == "true"

    if len(filter_in) > 0 and channel not in filter_in:
        logger.info("Filtering to include channels: %s", filter_in)
        return False

    if channel in filter_out:
        logger.info("Filtering to exclude channels: %s", filter_out)
        return False

    if disable_im and channel_type == "im":
        logger.info("IMs are: %s", "disabled" if disable_im else "enabled")
        return False

    return True


def respond_in_thread(body: dict, payload: dict, say: Say, client: WebClient) -> None:
    if not should_respond_for_channel(payload):
        return

    team_id = body["team_id"]
    app_id = body["api_app_id"]
    thread_ts = payload.get("thread_ts", payload["ts"])
    ts = say(
        **thinking_payload(),
        thread_ts=thread_ts,
    )["ts"]

    stream = stream_output_enabled()

    try:
        rulesets = get_rulesets(
            user_id=payload["user"],
            channel_id=payload["channel"],
            team_id=team_id,
            app_id=app_id,
        )
        # wip, if any rulesets have stream=True, then stream the response
        # changes the slack app behavior. any truthy value will work
        stream = stream or any(ruleset.meta.get("stream", False) for ruleset in rulesets)

        agent_output = agent(
            payload["text"],
            thread_alias=thread_ts,
            user_id=payload["user"],
            rulesets=rulesets,
            event_listeners=event_listeners(
                stream=stream,
                web_client=client,
                ts=ts,
                thread_ts=thread_ts,
                channel=payload["channel"],
            ),
            stream=stream,
        )
    except Exception as e:
        logger.exception("Error while processing response")
        client.chat_postMessage(
            **error_payload(str(e)),
            ts=ts,
            thread_ts=thread_ts,
            channel=payload["channel"],
            channel_type=payload.get("channel_type"),
        )
        return

    # Assuming that the response is already sent if its being streamed
    if not stream:
        for i, blocks in enumerate(markdown_blocks_list(agent_output)):
            if i == 0 and not persist_thoughts_enabled():
                client.chat_update(
                    text=agent_output,
                    blocks=blocks,
                    ts=ts,
                    channel=payload["channel"],
                )
            else:
                client.chat_postMessage(
                    text=agent_output,
                    blocks=blocks,
                    thread_ts=thread_ts,
                    channel=payload["channel"],
                )


def handle_slack_event(body: str, headers: dict) -> dict:
    req = BoltRequest(body=body, headers=headers)
    bolt_response = app.dispatch(req=req)
    return {
        "status": bolt_response.status,
        "body": bolt_response.body,
        "headers": bolt_response.headers,
    }
