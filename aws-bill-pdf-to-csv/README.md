This sample takes in a S3 URI pointing at a AWS Bill PDF and converts the bill into a CSV. Each item in the bill is converted to a row in the CSV. It will then write the CSV back to a provided S3 URI. This showcases how Griptape can be used to automate previously manual processes such as identifying if a PDF field with identical formatting is a `AWS Region` or an `AWS Service`.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create?sample-name=griptape-csv-filter&type=sample)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)
- AWS Access Key and Secret with S3 Read/Write permissions

## Configuration

env
```
AWS_ACCESS_KEY_ID=
```

env_secrets
```
OPENAI_API_KEY=
AWS_SECRET_ACCESS_KEY=
GT_CLOUD_API_KEY=
```

## Running this Sample

This sample converts an AWS bill PDF into a CSV. This is most useful for customers who have not enabled [Enhanced Billing CSV Reports](https://aws.amazon.com/about-aws/whats-new/2012/06/05/aws-billing-enables-enhanced-csv-reports-and-programmatic-access/) or for organization members who cannot download such reports. If available to you, the enhanced reports do contain more information that is not available in the PDF (and therefore cannot be derived into the CSV by this sample).

### Locally

You can run this Structure locally by providing the following inputs:

```
python structure.py -s <source_s3_uri> -d <destination_s3_uri>
```

### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.

```
-s
<source_s3_uri>
-d
<destination_s3_uri>
```

#### As a Data Source

Once created in Griptape Cloud, you can specify this [Structure as a Data Source](https://docs.griptape.ai/latest/griptape-cloud/data-sources/create-data-source/#Structure(Experimental)) if you wish to ingest the CSV formatted data as a Data Source. When running as a Data Source it will still save the output spreadsheet to your S3 bucket so you can validate the generated CSV.
