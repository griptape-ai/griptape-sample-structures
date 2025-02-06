This sample instruments a prompt-replying Griptape Agent with the [GriptapeCloudObservabilityDriver](https://docs.griptape.ai/latest/griptape-framework/drivers/observability-drivers/#griptape-cloud). The agent itself is as simple as it gets, this sample's purpose is to demonstrate how the observability can be introduced to Structures.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/griptape_observability)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

env_secrets
```
OPENAI_API_KEY=
GT_CLOUD_API_KEY=
```

## Running this Sample

The prompt defaults to: `What is the air speed velocity of an unladen swallow?`. You can specify your own prompt as an argument to the Structure.

### Locally

You can run this Structure using the [Skatepark emulator](https://github.com/griptape-ai/griptape-cli?tab=readme-ov-file#skatepark-emulator)

### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.

```
-p
"What is the answer to the universe?"
```
