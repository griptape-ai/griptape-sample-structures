This sample takes in serialized text artifacts from a CSV file (such as a Google Sheets file) formatted as Griptape Cloud Rule items, and synchonizes those artifacts with the Griptape Cloud resources of a [Ruleset](https://docs.griptape.ai/stable/griptape-cloud/api/api-reference/#/Rulesets) and associated [Rules](https://docs.griptape.ai/stable/griptape-cloud/api/api-reference/#/Rules). It is intended to serve as an example of a Structure as a Transform to use with [Griptape Cloud Data Sources](https://docs.griptape.ai/stable/griptape-cloud/data-sources/create-data-source/).

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=griptape-ruleset-sync&type=sample)

## Requirements

- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)

## Configuration

env_vars

```bash
GT_CLOUD_API_KEY=<encrypted_value> # Fill in with your own key
```

## Running this Sample

The first positional parameter will be the text artifacts input you wish to transform. You must specify the `-a` parameter to indicate the alias of the Ruleset you wish to synchronize with. If a Ruleset with that alias does not exist, then it will be created as part of the transform. Note that the `alias` field must be unique for a Ruleset within an Organization.

### Locally

This Structure is intended to be ran in Griptape Cloud as a Transform for a Data Source targeting a CSV file, such as a Google Sheet file. However, you can run this Structure locally by providing the following inputs:

```bash
python structure.py "Professional Rule: Always respond to the user in a professional manner.\n" -a "Professional Ruleset"
```

The format of this input represents a Griptape Cloud Rule name, `Professional Rule`, as well as Rule value, `Always respond to the user in a professional manner`. Rules are separated by the `\n` character, which occurs when a Data Source is loaded from a CSV.

### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.

```bash
"Professional Rule: Always respond to the user in a professional manner.\n"
-a
"Professional Ruleset"
```

#### As a Transform

Once created in Griptape Cloud, you can specify this Structure on any of your Data Sources and provide JUST the Ruleset alias (not the input artifacts), the system will handle the rest.

To use this Structure as a Transform for a Google Sheet declaring Rules, first create a Google Sheet in your Google Drive. Format the Google Sheet with names in the first row and values in the second row, as follows,:

| Rule 1 Name  | Rule 2 Name
| Rule 1 Value | Rule 2 Value

Then create a Google Drive type Data Source pointing to this Google Sheet as the selected item, and be sure to add the Structure Transform in the Advanced Options.

The arguments for the Structure Transform should be as follows:

```bash
-a
"Ruleset Alias"
```

This goes for any Structure you wish to run as a Transform. The Structure needs to supprt the first positional argument as a list of `Artifacts` and output a `TextArtifact` or `ListArtifact` (standard for text-based Structures).
