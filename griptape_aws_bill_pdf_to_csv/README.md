This sample takes a Bucket and Asset that represent an AWS Bill PDF stored in Griptape Cloud and converts the bill into a CSV. Each item in the bill is converted to a row in the CSV. The CSV is uploaded to the Bucket as a new Asset in addition to being returned by the Structure as a ListArtifact. This sample demonstrates both Griptape Cloud's Bucket and Asset resources and how Griptape can be used to automate previously manual/hardcoded processes. One such process is identifying if a PDF value with identical formatting is a `AWS Region` or an `AWS Service`.

[![Deploy_to_Griptape](https://github.com/griptape-ai/griptape-cloud/assets/2302515/4fd57873-5c93-44a8-8fa3-ac1bf7d73bcc)](https://cloud.griptape.ai/structures/create/griptape_aws_bill_pdf_to_csv)

## Requirements

- [Open AI Key](https://platform.openai.com/api-keys)
- [Griptape Cloud Key](https://cloud.griptape.ai/configuration/api-keys)
- [Griptape Cloud Bucket](https://cloud.griptape.ai/buckets) containing an AWS Bill PDF as an Asset. `upload.py` script may be used to create these resources.

## Configuration

env_secrets
```
OPENAI_API_KEY=
GT_CLOUD_API_KEY=
```

## Running this Sample

This sample converts an AWS bill PDF into a CSV. This is most useful for customers who have not enabled [Enhanced Billing CSV Reports](https://aws.amazon.com/about-aws/whats-new/2012/06/05/aws-billing-enables-enhanced-csv-reports-and-programmatic-access/) or for organization members who cannot download such reports. If available to you, the enhanced reports do contain more information that is not available in the PDF (and therefore cannot be derived into the CSV by this sample).

Assets are contained within a Bucket. This sample is configured to use the same Bucket for both the source Asset and the destination Asset. Asset file names must be unique within the same Bucket.

### Locally

You can run this Structure locally by providing the following inputs:

```
python structure.py -b <bucket_id> -d <workdir> -p <pdf_asset_file_name> -c <csv_asset_file_name>
```

You may also run the `upload.py` and `download.py` scripts locally to upload and download files directly:
```
python upload.py -b <bucket_id> -p <local_file_path> -d <workdir> -n <asset_file_name>

python download.py -b <bucket_id> -p <local_file_path> -d <workdir> -n <asset_file_name>
```

### Griptape Cloud

You can create a run via the API or the UI. When creating runs in the UI, you will need to specify parameters on their own lines.
`workdir` should be a relative path to the folder within the bucket containing the PDF; if `workdir` is not specified, the default will be the root of the Bucket.

```
-b
<bucket_id>
-d
<workdir>
-p
<pdf_asset_file_name>
-c
<csv_asset_file_name>
```

#### As a Data Source

Once created in Griptape Cloud, you can specify this [Structure as a Data Source](https://docs.griptape.ai/latest/griptape-cloud/data-sources/create-data-source/#Structure(Experimental)) if you wish to ingest the CSV formatted data as a Data Source. When running as a Data Source it will still save the output spreadsheet to your Bucket so you may download the generated CSV for validation with `download.py`.
