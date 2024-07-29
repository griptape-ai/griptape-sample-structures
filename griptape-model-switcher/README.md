This sample allows you to switch between three different providers and models with a simple explanation prompt in order to contrast responses. You can specify provider with the `-p` parameter and choose between `google`, `openai`, and `anthropic`. The models for each provider currently default to `gemini-1.5-pro`, `gpt-4o`, and `claude-3-5-sonnet-20240620` respectively. Read more about [Griptape's Structure Config](https://docs.griptape.ai/stable/griptape-framework/structures/config/) to see what other providers Griptape is integrated with.

You can optionally specify the `-s` or `a` paramters to change the subject or audience of the prompt.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=griptape-model-switcher&type=sample)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
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
OPENAI_API_KEY=<encrypted_value> # Fill in with your own key
ANTHROPIC_API_KEY=<encrypted_value> # Fill in with your own key
VOYAGE_API_KEY=<encrypted_value> # Fill in with your own key
GOOGLE_API_KEY=<encrypted_value> # Fill in with your own key
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```
