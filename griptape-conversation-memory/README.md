This sample allows you to deploy a Griptape Agent configured with the Griptape Cloud Conversation Memory Driver.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud-zach-dev.griptape.ai/structures/create?sample-name=griptape-conversation-memory&type=sample)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud API Key](https://cloud.griptape.ai/account/api-keys)

## Configuration

Environment Variables

```
OPENAI_API_KEY=<secret_ref> # Reference your own key from a Griptape Secret
GT_CLOUD_API_KEY=<secret_ref> # Reference your own key from a Griptape Secret
```

## Running this Sample

The prompt defaults to: `Hello there!`. You can specify your own prompt as an argument to the Structure.

### Locally

You can run this with no parameters and use the defaults.

```bash
python structure.py
```

Defaults:

```bash
-p "Hello, my name is Griptaper!"
```

You can update the arguments when you run

```bash
python structure.py -p "Hello, my name is Griptaper!"
```

To make use of the conversation memory, create a Griptape Cloud Thread, and pass that as a parameter to continue the conversation!

```bash
python structure.py -t <thread_id> -p "Hello, my name is Griptaper!"
```

### Griptape Cloud

You can create a run via the API or the UI.

```bash
-t
<thread_id>>
-p
Hello, my name is Griptaper!
```
