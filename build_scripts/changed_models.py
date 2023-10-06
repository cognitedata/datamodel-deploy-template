import argparse
import json
import os
import subprocess

from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Upload models to CDF")
    parser.add_argument(
        "folders",
        type=str,
        nargs=1,
        help="The folders to monitor for deployment of data models",
    )
    parser.add_argument("deploy_all", type=str, nargs="?", help="The folders/files to deploy to all", default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    check_folders = Path(args.folders[0])
    if not check_folders.exists():
        print("Input: Folders to consider (re)deploying does not exist")
        exit(1)

    deploy_all_folder = None
    if args.deploy_all:
        deploy_all_folder = Path(args.deploy_all.strip())
        print(f"Input: Common folder/file (may force deploy all): {deploy_all_folder!r}")

    # Compare against previous commit under the assumption of squash-only merges:
    diff = subprocess.check_output("git diff --name-only HEAD^ HEAD".split(), text=True).split()
    changed_files = set(map(Path, diff))

    if deploy_all_folder is not None and any(f.is_relative_to(deploy_all_folder) for f in changed_files):
        to_deploy = check_folders
        print("Common folder has one or more changed file(s), will deploy all functions")
    else:
        to_deploy = [fld.replace("datamodels/","") for fld in check_folders if any(f.is_relative_to(fld) for f in changed_files)]

    if to_deploy:
        print(f"To be deployed: {to_deploy}")
    else:
        print("No changed folders detected, skipping deployment!")
        to_deploy = ["skipDeploy"]

    if "GITHUB_OUTPUT" not in os.environ:
        # For local testing
        print(f"matrix={json.dumps({'folders': str(to_deploy)})}")
        print(f"folders={to_deploy}")
        return
    else:
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            print(f"matrix={json.dumps({'folders': to_deploy})}", file=fh)
            print(f"folders={to_deploy}", file=fh)


if __name__ == "__main__":
    main()
