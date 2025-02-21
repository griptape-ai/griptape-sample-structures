import argparse
import re

from dotenv import load_dotenv
from griptape.utils import GriptapeCloudStructure


def replace_substrings_case_insensitive(input_string: str, find_string: str, replace_string: str) -> str:
    pattern = re.compile(re.escape(find_string), re.IGNORECASE)
    return pattern.sub(replace_string, input_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_artifacts")  # positional
    parser.add_argument(
        "-f",
        "--find_word",
        help="The word you wish to find in the artifacts",
    )
    parser.add_argument(
        "-r",
        "--replace_with",
        help="The word you wish to replace with",
    )

    args = parser.parse_args()

    load_dotenv()

    result = replace_substrings_case_insensitive(args.input_artifacts, args.find_word, args.replace_with)

    with GriptapeCloudStructure() as structure:
        structure.output = result
