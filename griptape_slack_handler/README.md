# Griptape Cloud Structure-as-a-Slackbot

Integrating intelligent LLM-powered applications with Slack is a very popular use-case for Griptape Cloud. This sample provides a complete implementation of an event handler for a Slack Application within a Griptape Structure, ready for you to deploy it on Griptape Cloud.

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud API Key](https://cloud.griptape.ai/configuration/api-keys)
- [Slack Account and Workspace](https://slack.com/)

## Configuration

Environment Variables

```bash
OPENAI_API_KEY=<secret_ref> # Reference your own key from a Griptape Secret
GT_CLOUD_API_KEY=<secret_ref> # Reference your own key from a Griptape Secret
```

## Running this Sample

This sample is intended to run as a Griptape Cloud hosted Structure.

### Deploying your Structure code to Griptape Cloud

Follow the instructions in the main README of this repo to deploy this Structure to your Griptape Cloud account.

### Creating the Slack App Integration

1. Go to [Griptape Cloud Integrations](https://cloud.griptape.ai/structures/create) and fill out the form for creating a Slack integration.
   1. Skip the entry about Bot Token and Signing Secret, you will update those later.
   1. If you have already created your Slack Bot Structure, select it now under the "Structures" field.
1. Copy the Slack App Manifest on the Integration config page.
1. Go to your [Slack Apps Page](https://api.slack.com/apps) and Press "Create New App" -> "From a manifest".
1. Paste in the Slack App Manifest, and click through until the app is created.
1. Get the Signing Secret from the "Basic Information" tab from your newly created App.
1. Go back to your integration page on Griptape Cloud and type in a secret name under "Slack App Secret" and hit enter.
1. Paste in the value of the Signing Secret.
1. Go back to your Slack App and press the "OAuth & Permissions" tab.
1. Click the "Install to `workspace`" button, and click through to install the App into your Slack workspace.
1. Copy the newly created Bot Token.
1. Go back to your integration page on Griptape Cloud and type in a secret name under "Slack Bot Token" and hit enter.
1. Paste in the value of the Bot Token.
1. Lastly, go back to your slack app and press the "Event Subscriptions" tab.
1. Hit "retry" next to the URL displayed in the field. It should have a green checkmark and say "Verified".

That's it! Now find your app in Slack and start chatting. It can be added to channels as well as messaged in private chats.

## Slack Bot Runtime Configuration

The bot will always respond with a three-dots gif to indicate it has started processing messages. It will then update this message over time, explaining its actions, and then ultimately overwrite the message with its final response.

There are a few ways to configure other behavior of the bot at runtime.

### Channel Filtering

Set environment variables to include or exclude specific Slack channels that the Slackbot Structure should respond in:

The `FILTER_IN_CHANNELS` configuration overrides the `FILTER_OUT_CHANNELS` if both are provided. The following configuration will allow the bot to only respond in channels "A012BA2A9DG" and "B012BA2A9DG".

```bash
FILTER_IN_CHANNELS="A012BA2A9DG,B012BA2A9DG"
```

The following configuration will restrict the bot from responding in only these channels "A012BA2A9DG" and "B012BA2A9DG".

```bash
FILTER_OUT_CHANNELS="A012BA2A9DG,B012BA2A9DG"
```

The following configuration will disable communication with the bot in direct messages:

```bash
DISABLE_IM="true"
```

#### How to find the Channel ID

To find the Channel ID for a particular Slack channel:

1. Right click the channel
1. Click `View channel details`
1. Locate the Channel ID at the bottom of the window

### Dynamic Rulesets

Using the `GriptapeCloudRulesetDriver` allows the bot to pull in Rulesets for every event that comes through. For every message, the bot will reach out to Griptape Cloud and try to find [Rulesets](https://cloud.griptape.ai/rulesets) that are aliased with the following values:

- Slack App ID
- Slack Team ID
- Slack Channel ID
- Slack User ID

Simply create a Griptape Cloud Ruleset and set the `alias` field to any one of those values, and the bot will find and use them.

### Conversation Memory

The bot will always respond in a Slack thread, creating a new one if needed. Outside of a DM, the bot will only respond if explicitly tagged with `@bot_name`. However, the bot is picking up other messages and storing them in a Griptape Cloud [Thread](https://cloud.griptape.ai/threads), and will be able to understand previous context if tagged in a message later in a Slack thread.

### Experimental

#### Dynamic Tool Selection

Creating a "Kitchen Sink" Agent with Griptape is really easy, but sometimes the LLM can get confused if it is given too many instructions. The [`get_tools`](griptape_slack_handler/griptape_tool_box.py) function with parameter `dyanamic=True` will prompt the LLM to decide which tools it should use to accomplish a given input, and those tools will be passed to the final "Kitchen Sink" agent that will respond to the user. It will use other context, such as conversation history, to make its decision.

This can be enabled by setting `"enable_toolbox": "true"` in the metadata of any Ruleset that gets pulled in.

#### Streaming Responses

Responses from the Griptape Agent can be streamed token-by-token for faster perceived response times. These tokens will be batched and sent as larger message chunks back to slack, updating the bot's initial response message over time.

This can be enabled by setting `"stream": "true"` in the metadata of any Ruleset that gets pulled in.
