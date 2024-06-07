In this example we implement a multi-agent Workflow. We have a single "Researcher" Agent that conducts research on a topic, and then fans out to multiple "Writer" Agents to write blog posts based on the research.

By splitting up our workloads across multiple Structures, we can parallelize the work and leverage the strengths of each Agent. The Researcher can focus on gathering data and insights, while the Writers can focus on crafting engaging narratives.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures?url=https://github.com/griptape-ai/griptape-sample-structures/blob/main/griptape-webscraper-researcher/structure.py&name=Griptape%20Webscraper%20Researcher)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/keys)
- [Google Custom Search](https://developers.google.com/custom-search/v1/introduction)

## Configuration

env
```
GOOGLE_API_SEARCH_ID=<value>
```

env_secrets
```
OPENAI_API_KEY=<encrypted_value>
GT_CLOUD_API_KEY=<encrypted_value>
GOOGLE_API_KEY=<encrypted_value>
```
