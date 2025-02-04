This example is basic Langchain code, but mainly intended to show you how you could deploy and host your Langchain code on Griptape Cloud.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/langchain-calculator)

> ⚠️ **NOTE:** The repository URL is hardcoded to griptape-ai in the Deploy to Griptape Cloud button. It is not dynamically updated as a variable. If you fork this repo, update the URL accordingly. 
> 

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

env_secrets
```
OPENAI_API_KEY=<encrypted_value> # Fill in with your own key
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```

## Running this Sample

### Locally

```
python structure.py
```

### Griptape Cloud

Create a run with no parameters

