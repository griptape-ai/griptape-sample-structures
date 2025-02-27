import argparse
import os

from dotenv import load_dotenv
from griptape.drivers.file_manager.griptape_cloud import GriptapeCloudFileManagerDriver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bucket_id",
        default=None,
        help="The Griptape Cloud Bucket destination of the file being downloaded.",
    )
    parser.add_argument(
        "-p",
        "--local_file_path",
        default=None,
        help="The local file path of the file being downloaded.",
    )
    parser.add_argument(
        "-d",
        "--workdir",
        default=None,
        help="The working directory download location in the Griptape Cloud Bucket.",
    )
    parser.add_argument(
        "-n",
        "--file_name",
        default=None,
        help="The name for the file being downloaded in the Griptape Cloud Bucket.",
    )

    args = parser.parse_args()
    bucket_id = args.bucket_id
    local_file_path = args.local_file_path
    workdir = args.workdir
    file_name = args.file_name

    load_dotenv()

    gtc_file_manager_driver = GriptapeCloudFileManagerDriver(
        api_key=os.environ["GT_CLOUD_API_KEY"],
        bucket_id=bucket_id,
        workdir=workdir,
    )

    with open(file=local_file_path, mode="wb") as file:
        file.write(gtc_file_manager_driver.try_load_file(file_name))
