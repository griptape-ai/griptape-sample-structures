In this example we implement a multi-agent Workflow. We have a single "Researcher" Agent that conducts research on a topic, and then fans out to multiple "Writer" Agents to write blog posts based on the research.

By splitting up our workloads across multiple Structures, we can parallelize the work and leverage the strengths of each Agent. The Researcher can focus on gathering data and insights, while the Writers can focus on crafting engaging narratives.

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/keys)
- [Google Custom Search](https://developers.google.com/custom-search/v1/introduction)

## Deploy to Griptape Cloud

This example requires three separate Structures in Griptape Cloud.

### Researcher Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures?url=https://github.com/griptape-ai/griptape-sample-structures/blob/main/griptape-multi-agent-workflows/researcher.py&name=Researcher)

```
GOOGLE_API_SEARCH_ID=<id>
GOOGLE_API_KEY=<key>
OPENAI_API_KEY=<key>
```

### Writer Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures?url=https://github.com/griptape-ai/griptape-sample-structures/blob/main/griptape-multi-agent-workflows/writer.py&name=Writer)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
```

### Main Workflow

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures?url=https://github.com/griptape-ai/griptape-sample-structures/blob/main/griptape-multi-agent-workflows/workflow.py&name=Multi%20Agent%20Workflow)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
GT_RESEARCH_STRUCTURE_ID=<researcher_structure_id>
GT_WRITER_STRUCTURE_ID=<writer_structure_id>
```
