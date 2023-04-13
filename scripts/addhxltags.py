import argparse
import json
from pathlib import Path

import hxl
import hxl.converters
import hxl.input
from validate_catalog import validate_url

from utils import (
    CSVResponseInput,
    get_gdown_response,
    is_gdrive_url,
    is_github_url,
    transform_gdrive_url,
    transform_github_url,
)

parser = argparse.ArgumentParser(description="Add hxl tags to a file")
parser.add_argument(
    "-i", "--input", metavar="filename1/url", type=str, help="input file path or url"
)
parser.add_argument(
    "-o", "--output", metavar="filename2", type=str, help="output file path"
)
parser.add_argument(
    "-t", "--tags", metavar="filename3", type=str, help="json tags file path"
)


def main():
    args = parser.parse_args()

    if not args.input:
        print("Missing input file or url, specify -i or --input")
        return 1
    if not args.output:
        print("Missing output file, specify -o or --output")
        return 1
    if not args.tags:
        print("Missing tags file, specify -t or --tags")
        return 1
    if args.input.startswith("http://") or args.input.startswith("https://"):
        unpatched = args.input
        if is_github_url(unpatched):
            unpatched = transform_github_url(unpatched)
        elif is_gdrive_url(unpatched):
            unpatched = transform_gdrive_url(unpatched)
        if not validate_url(unpatched, args.input):
            return 1
        input_options = None
    else:
        # assume file
        unpatched = Path(args.input)
        if not unpatched.exists():
            print(f"Invalid input file: {unpatched} not found")
            return 1
        unpatched = unpatched.as_posix()
        input_options = hxl.input.InputOptions(allow_local=True)
    patched = Path(args.output)
    if not patched.parent.is_dir():
        print(
            f"output directory {patched.parent} for output file {patched.name} does not exist. Create it first."
        )
        return 1

    tagfile = Path(args.tags)
    if not tagfile.exists():
        print(f"Invalid tags file: {tagfile} not found")
        return 1
    tagging_specs = []
    with open(tagfile) as f:
        tagging_specs = json.load(f)
    if is_gdrive_url(unpatched):
        resp, sess = get_gdown_response(unpatched)
        if resp is None:
            print(
                f"Invalid gdrive url {unpatched}: Could not access url. Possibly not publically shared."
            )
        csv_input = CSVResponseInput(resp, sess)
    else:
        csv_input = hxl.input.make_input(unpatched, input_options=input_options)
    source = hxl.data(
        hxl.converters.Tagger(
            csv_input,
            tagging_specs,
        )
    ).cache()

    with open(
        patched,
        "w",
        encoding="utf-8",
    ) as f:
        # Write out a dataset as CSV
        hxl.input.write_hxl(f, source)
    return 0


if __name__ == "__main__":
    exit(main())
