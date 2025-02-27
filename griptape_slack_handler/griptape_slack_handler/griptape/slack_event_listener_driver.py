from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING

from attrs import define, field
from griptape.drivers.event_listener import BaseEventListenerDriver

if TYPE_CHECKING:
    from slack_sdk import WebClient

log = logging.getLogger()


@define(kw_only=True)
class SlackEventListenerDriver(BaseEventListenerDriver):
    """
    A driver for sending messages back to Slack.

    Attributes:
        web_client: The Slack WebClient to use for interacting with the Slack API.
        ts: The timestamp of the message to update.
        thread_ts: The timestamp of the thread.
        channel: The channel ID.

    """

    web_client: WebClient = field()
    ts: str = field()
    thread_ts: str = field()
    channel: str = field()
    batched: bool = field(default=False)

    _slack_responses: dict = field(factory=dict, init=False)
    _thread_lock: threading.Lock = field(factory=threading.Lock, init=False)

    def try_publish_event_payload_batch(self, event_payload_batch: list[dict]) -> None:
        with self._thread_lock:
            new_text = "".join([event.get("text", "") for event in event_payload_batch])
            try:
                res = self._slack_responses[self.ts] = self.web_client.chat_update(
                    text=self._slack_responses.get(self.ts, {}).get("text", "") + new_text,
                    ts=self.ts,
                    thread_ts=self.thread_ts,
                    channel=self.channel,
                )
                self._slack_responses[self.ts] = res
            except Exception:
                log.exception("Error updating message")
                res = self.web_client.chat_postMessage(
                    text=new_text,
                    thread_ts=self.thread_ts,
                    channel=self.channel,
                )
                self._slack_responses[res["ts"]] = res
                self.ts = res["ts"]

    def try_publish_event_payload(self, event_payload: dict) -> None:
        with self._thread_lock:
            payload = {**event_payload}
            try:
                if "blocks" in event_payload:
                    payload["blocks"] = self._get_last_blocks() + event_payload["blocks"]
                res = self.web_client.chat_update(
                    **payload,
                    ts=self.ts,
                    thread_ts=self.thread_ts,
                    channel=self.channel,
                )
                self._slack_responses[res["ts"]] = res.data

            except Exception:
                log.exception("Error updating message")
                res = self.web_client.chat_postMessage(
                    **event_payload,
                    thread_ts=self.thread_ts,
                    channel=self.channel,
                )
                self._slack_responses[res["ts"]] = res.data
                self.ts = res["ts"]

    def _get_last_blocks(self) -> list[dict]:
        return self._slack_responses.get(self.ts, {}).get("message", {}).get("blocks", [])
