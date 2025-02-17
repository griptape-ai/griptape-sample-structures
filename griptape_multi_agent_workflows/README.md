Systems of agents are an effective way for large language models to autonomously handle large or complex tasks. Implementing systems of agents is simple with Griptape.

In this example we implement a multi-agent Workflow. We have a single "Researcher" Agent that conducts research on a topic, and then fans out to multiple "Writer" Agents to write blog posts based on the research.

By splitting up our workloads across multiple structures, we can parallelize the work and leverage the strengths of each Agent. The Researcher can focus on gathering data and insights, while the Writers can focus on crafting engaging narratives. The Workflow structure ties the the runs of the other two Agents together to get the final result.

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)
- [Google Custom Search](https://developers.google.com/custom-search/v1/introduction)

## Configuration

This example requires three separate structures each with their own configuration. You should deploy the Researcher and Writer structures first to Griptape Cloud and then provide the IDs of those structures to the Workflow structure.

### Researcher Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/github-creation?org=griptape-ai&repo=griptape-sample-structures&branch=main&structure-config-file=griptape_multi_agent_workflows/structure_config_researcher.yaml&name=Researcher&env-var=GOOGLE_API_SEARCH_ID&env-var=GOOGLE_API_KEY&env-var=OPENAI_API_KEY&env-var=GT_CLOUD_API_KEY)

```
GOOGLE_API_SEARCH_ID=<id>
GOOGLE_API_KEY=<key>
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
```

### Writer Agent

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/github-creation?org=griptape-ai&repo=griptape-sample-structures&branch=main&structure-config-file=griptape_multi_agent_workflows/structure_config_writer.yaml&name=Writer&env-var=OPENAI_API_KEY&env-var=GT_CLOUD_API_KEY)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
```

### Main Workflow

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/github-creation?org=griptape-ai&repo=griptape-sample-structures&branch=main&structure-config-file=griptape_multi_agent_workflows/structure_config_workflow.yaml&name=Workflow&env-var=OPENAI_API_KEY&env-var=GT_CLOUD_API_KEY&env-var=GT_RESEARCH_STRUCTURE_ID&env-var=GT_WRITER_STRUCTURE_ID)

```
OPENAI_API_KEY=<key>
GT_CLOUD_API_KEY=<key>
GT_RESEARCH_STRUCTURE_ID=<researcher_structure_id>
GT_WRITER_STRUCTURE_ID=<writer_structure_id>
```

## Running this Sample

### Locally

This sample as written is intended to have each of the structures deployed to Griptape Cloud. If you wish to recreate these structures in a purely local workflow, then you will need to replace the `GriptapeCloudStructureRunDriver` with `LocalStructureRunDriver`. [Read more about Structure Run Drivers](https://docs.griptape.ai/stable/griptape-framework/drivers/structure-run-drivers/).


### Griptape Cloud

You can run any of the agents individually, but to run the entire system you will create a run from the `Workflow` structure with no parameters.
