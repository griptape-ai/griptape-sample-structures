Griptape Cloud has the capability to store conversation memory in threads, persisting this across sessions, providing summarization features that avoid excessive token consumption, and reducing the likelihood that applications with long running conversation histories will exceed context length limits.
This sample combines these features with a Ruleset Driver and a Knowledge Base Tool, allowing you to chat with an agent that has a long term persistent memory of your conversation. 

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/griptape_chat_memory_agent)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud API Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

Environment Variables

```bash
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

You can update the arguments when you run.

```bash
python structure.py -p "Hello, my name is Griptaper!"
```

To make use of the conversation memory, create a Griptape Cloud Thread, and pass that as a parameter to continue the conversation!

```bash
python structure.py -t <thread_id> -p "Hello, my name is Griptaper!"
```

To enable the Agent to make use of a [Griptape Cloud Knowledge Base](https://docs.griptape.ai/latest/griptape-cloud/knowledge-bases/create-knowledge-base/) for [Retrieval Augmented Generation](https://docs.griptape.ai/latest/griptape-framework/engines/rag-engines/), create a Griptape Cloud Knowledge Base, and pass the Knowledge Base ID as a parameter to the run.

```bash
python structure.py -p "According to the Knowledge Base, what is RAG?" -k "123d66e6-2a16-4e9e-b077-0b1e9869d251"
```

To make use of a Ruleset for the Agent, create a [Griptape Cloud Ruleset](https://docs.griptape.ai/latest/griptape-cloud/rules/rulesets/), and pass the Ruleset `alias` as a parameter to shape the Agent's behavior.

```bash
python structure.py -p "Hello, my name is Griptaper!" -r "GriptapeExpertAgent"
```

To enable the Agent to stream responses, include the streaming flag:

```bash
python structure.py -t <thread_id> -p "Hello, my name is Griptaper!" -s
```

### Griptape Cloud

You can create a run via the API or the UI.

```bash
-k
123d66e6-2a16-4e9e-b077-0b1e9869d251
-t
<thread_id>>
-p
Hello, my name is Griptaper!
-r 
"GriptapeExpertAgent"
-s
```
