This sample allows you to switch between three different providers and models with a simple explanation prompt in order to contrast responses. You can specify provider with the `-p` parameter and choose between `google`, `openai`, and `anthropic`. Read more about [Griptape's Structure Config](https://docs.griptape.ai/stable/griptape-framework/structures/configs/) to see what other providers Griptape is integrated with.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/griptape-model-switcher)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Anthropic API Key](https://console.anthropic.com/settings/keys)
- [Google API Key](https://ai.google.dev/gemini-api/docs)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

```
OPENAI_API_KEY=<encrypted_value> # Fill in with your own key
ANTHROPIC_API_KEY=<encrypted_value> # Fill in with your own key
GOOGLE_API_KEY=<encrypted_value> # Fill in with your own key
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```

## Running this Sample

The prompt defaults to: `Briefly explain how { subject } work to { audience }`. You can optionally specify the `-s` or `-a` parameters to change the `subject` or `audience` of the prompt.

### Locally

You can run this with no parameters and use the defaults.

```
python structure.py
```

Defaults:
```
-p google -s computers -a "a five-year-old child"
```

You can update any subset of these parameters when you run
```
python structure.py -p openai -a "a punk rock band"
```

### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.

```
-p
openai
-s
ovens
-a
a punk rock band
```

This will change the provider being used to `openai` and the prompt to be `Briefly explain how ovens work to a punk rock band.`
