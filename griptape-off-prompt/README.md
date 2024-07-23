This sample summarizes your website of choice into a text message to a friend. You can toggle seamlessly between two Griptape Agents; one that utilizes [Griptape's Task Memory](https://docs.griptape.ai/latest/griptape-framework/structures/task-memory/) and one that does not. When running this sample, you may specify the `-o` command line option to toggle `off_prompt=True`. You may also specify your own website to summarize with `-w <website-url>`.

To learn more, see the [Griptape blog post on Task Memory and Off-Prompt](https://www.griptape.ai/blog/the-power-of-task-memory-and-off-prompt-tm).

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures?url=https://github.com/griptape-ai/griptape-sample-structures/blob/main/griptape-off-prompt/structure.py&name=Griptape%20Off-Prompt%20Sample)

## Requirements

- [Anthropic API Key](https://console.anthropic.com/settings/keys)
- [Voyage API Key](https://dash.voyageai.com/)
- [Griptape Cloud Key](https://cloud.griptape.ai/keys)

## Configuration

env
```
# None Needed
```

env_secrets
```
ANTHROPIC_API_KEY=<encrypted_value> # Fill in with your own key
VOYAGE_API_KEY=<encrypted_value> # Fill in with your own key
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```
