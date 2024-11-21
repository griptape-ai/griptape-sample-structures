import sys
import json
import rich.logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        rich.logging.RichHandler(
            tracebacks_code_width=500,
            tracebacks_show_locals=True,
            tracebacks_word_wrap=False,
            tracebacks_width=500,
            locals_max_length=500,
            locals_max_string=500,
        )
    ],
    force=True,
)


if __name__ == "__main__":
    from griptape_slack_handler import handle_slack_event

    body, query, headers = sys.argv[1:4]
    res = handle_slack_event(body, json.loads(headers))

    if res["status"] >= 400:
        sys.exit(1)
