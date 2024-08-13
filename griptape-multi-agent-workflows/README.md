In this example we implement a multi-agent Workflow. We have a single "Researcher" Agent that conducts research on a topic, and then fans out to multiple "Writer" Agents to write blog posts based on the research.

By splitting up our workloads across multiple Structures, we can parallelize the work and leverage the strengths of each Agent. The Researcher can focus on gathering data and insights, while the Writers can focus on crafting engaging narratives.

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/account/api-keys)
- [Google Custom Search](https://developers.google.com/custom-search/v1/introduction)

## Configuration

This example requires three separate Structures each with their own configuration.

### Researcher Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?org=griptape-ai&repo=griptape-sample-structures&branch=main&file=griptape-multi-agent-workflows%2Fresearcher.py&name=Researcher&type=github)

```
GOOGLE_API_SEARCH_ID=<id>
GOOGLE_API_KEY=<key>
OPENAI_API_KEY=<key>
```

### Writer Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?org=griptape-ai&repo=griptape-sample-structures&branch=main&file=griptape-multi-agent-workflows%2Fwriter.py&name=Writer&type=github)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
```

### Main Workflow

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?org=griptape-ai&repo=griptape-sample-structures&branch=main&file=griptape-multi-agent-workflows%2Fworkflow.py&name=Workflow&type=github)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
GT_RESEARCH_STRUCTURE_ID=<researcher_structure_id>
GT_WRITER_STRUCTURE_ID=<writer_structure_id>
```

## Running this Sample

### Locally

```
python workflow.py
```

### Griptape Cloud

You can run any of the agents individually, but to run the entire system you will create a run from the `Workflow` structure with no parameters.
