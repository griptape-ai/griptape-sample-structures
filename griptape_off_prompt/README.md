Griptape offers the ability to store information in a configurable vector store called TaskMemory. This can be helpful in cases where you do not want to share information with model providers for security or compliance reasons. It can also help reduce token counts and allow your applications to handle context length constraints. 

This sample summarizes your website of choice into a text message to a friend. You can toggle seamlessly between two Griptape Agents; one that utilizes [Griptape's Task Memory](https://docs.griptape.ai/latest/griptape-framework/structures/task-memory/) and one that does not. 

To learn more, see the [Griptape blog post on Task Memory and Off-Prompt](https://www.griptape.ai/blog/the-power-of-task-memory-and-off-prompt-tm).

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/griptape_off_prompt)

> ⚠️ **NOTE:** The repository URL is hardcoded to griptape-ai in the Deploy to Griptape Cloud button. It is not dynamically updated as a variable. If you fork this repo, update the URL accordingly. 
> 
## Requirements

- [Anthropic API Key](https://console.anthropic.com/settings/keys)
- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

```
ANTHROPIC_API_KEY=<encrypted_value> # Fill in with your own key
# OPENAI KEY IS REQUIRED FOR OFF-PROMPT FLAG
OPENAI_API_KEY=<encrypted_value> # Fill in with your own key. 
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```

## Running this Sample

### Locally

The prompt this agent runs is: `Summarize the following website into a text message you would send a friend limited to 160 characters: { website }`

You can run this with no parameters and use the defaults. By default, this sample will run with `off_prompt=False` as that is the default for the Griptape Framework. The default webpage that is scraped is the [Off Prompt blog post](https://www.griptape.ai/blog/the-power-of-task-memory-and-off-prompt-tm).

When running this sample, you may specify the `-o` command line option to toggle `off_prompt=True`. You may also specify your own website to summarize with `-w <website-url>`.

```
python structure.py
```

You can specify to run the sample off_prompt with the `-o` parameter
```
python structure.py -o
```

You can change the website that is scraped by specifying the `-w` parameter
```
python structure.py -w https://en.wikipedia.org/wiki/Large_language_model
```

### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.

```
-o
-w
https://en.wikipedia.org/wiki/Large_language_model
```
