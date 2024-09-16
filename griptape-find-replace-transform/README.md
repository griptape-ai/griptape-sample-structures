This sample takes in

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=griptape-find-replace-transform&type=sample)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

env
```
# None Needed
```

env_secrets
```
OPENAI_API_KEY=<encrypted_value> # Fill in with your own key
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```

## Running this Sample

The prompt defaults to: `Replace the word {find_word} with {replace_with} in {artifacts}`. The first positional parameter will be the input you wish to transform. You can optionally specify the `-f` or `-r` parameters to change the `find_word` or `replace_with` values of the prompt.

### Locally

You can run this Structure locally by providing the following inputs:

```
python structure.py "This is a find and replace test for the word: Griptape" -f "Griptape" -r "Wonderbread"
```

Note that the positional input can appear after the `-f` and `-r` arguments if necessary.


### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.

```
-f
"Griptape"
-r
"Wonderbread"
"This is a find and replace test for the word: Griptape"
```

#### As a Transform

Once created in Griptape Cloud, you can specify this Structure on any of your Data Sources and provide JUST the find and replace words (not the input artifacts), the system will handle the rest.

```
-f
"Griptape"
-r
"Wonderbread"
```

This goes for any Structure you wish to run as a Transform. The Structure needs to supprt the first positional argument as a list of `Artifacts` and output a `TextArtifact` or `ListArtifact` (standard for text-based Structures).