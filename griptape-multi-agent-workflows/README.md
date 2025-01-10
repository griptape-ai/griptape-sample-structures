In this example we implement a multi-agent Workflow. We have a single "Researcher" Agent that conducts research on a topic, and then fans out to multiple "Writer" Agents to write blog posts based on the research.

By splitting up our workloads across multiple structures, we can parallelize the work and leverage the strengths of each Agent. The Researcher can focus on gathering data and insights, while the Writers can focus on crafting engaging narratives. The Worklow structure ties the the runs of the other two Agents together to get the final result.

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)
- [Google Custom Search](https://developers.google.com/custom-search/v1/introduction)

## Configuration

This example requires three separate structures each with their own configuration. You should deploy the Researcher and Writer structures first to Griptape Cloud and then provide the IDs of those structures to the Workflow structure.

### Researcher Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=github-creation&org=griptape-ai&repo=griptape-sample-structures&branch=main&structure-config-file=griptape-multi-agent-workflows/structure_config_researcher.yaml&name=Researcher)

```
GOOGLE_API_SEARCH_ID=<id>
GOOGLE_API_KEY=<key>
OPENAI_API_KEY=<key>
```

### Writer Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=github-creation&org=griptape-ai&repo=griptape-sample-structures&branch=main&structure-config-file=griptape-multi-agent-workflows/structure_config_writer.yaml&name=Writer)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
```

### Main Workflow

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=github-creation&org=griptape-ai&repo=griptape-sample-structures&branch=main&structure-config-file=griptape-multi-agent-workflows/structure_config_workflow.yaml&name=Workflow)

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
