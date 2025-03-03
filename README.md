# Griptape Samples

This repo contains sample structures for customers to view and use as examples to getting started with both [Griptape](https://github.com/griptape-ai/griptape) and [Griptape Cloud](https://cloud.griptape.ai/).

## Getting Started

You can deploy and run these samples using Griptape Cloud.

To get started with hosting and running a sample on Griptape Cloud, you will first need to [create Griptape Cloud account](https://auth.cloud.griptape.ai/u/login).

Once logged in, you can [create a structure from a sample](https://cloud.griptape.ai/structures/create) in Griptape Cloud. You can also click the "Deploy to Griptape Cloud" in each of the sub folders in this repo to get started in 2-clicks with a specific sample.

## Table of Contents

| Sample | Folder |
| -------- | ------- |
| Multiple Agents on Griptape Cloud | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_multi_agent_workflows) |
| Run your Langchain code on Griptape Cloud | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/langchain_calculator) |
| Model Switcher with Griptape | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_model_switcher) |
| Griptape Task Memory and Off Prompt | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_off_prompt) |
| Griptape Chat Memory Agent | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_chat_memory_agent) |
| Find and Replace Transform | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_find_replace_transform) |
| Griptape Filter CSVs | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_csv_filter) |
| Griptape AWS Bill PDF to CSV | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_aws_bill_pdf_to_csv) |
| Griptape Slack Handler | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_slack_handler) |
| Observability in Griptape | [LINK](https://github.com/griptape-ai/griptape-sample-structures/tree/main/griptape_observability) |


## Running Samples

Each Sample's README has more details on how to call and run the Sample. If you wish to run the Sample via the Griptape Framework, take a look at [Structure Run Drivers](https://docs.griptape.ai/stable/griptape-framework/drivers/structure-run-drivers/).

## Local Dev

### uv

This project uses [uv](https://docs.astral.sh/uv/) to manage project dependencies.
If you're familiar with using [poetry](https://python-poetry.org/), `uv` is a more modern alternative.
After you've [installed uv](https://docs.astral.sh/uv/getting-started/installation/), you can install the project dependencies by running:

```bash
uv sync --all-extras --all-groups
```

While each sample defines its own dependencies in a directory-local `requirements.txt`, this command will install some common dependencies that are used across all samples for an easier local development experience.

### ruff

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

You can run the `ruff` formatter on the project by running:

```bash
uv run ruff format
```

You can run the `ruff` linter on the project by running:

```bash
uv run ruff check --fix
```

### pyright

This project uses [pyright](https://github.com/microsoft/pyright) for static type checking.

You can run `pyright` on the project by running:

```bash
uv run pyright
```


### typos

This project uses [typos](https://github.com/crate-ci/typos) for spell checking.

You can run `typos` on the project by running:

```bash
uv run typos
```
