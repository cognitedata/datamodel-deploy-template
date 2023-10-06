import argparse
import json
import os
import subprocess
import itertools
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

CONFIG_FILE = (REPO_ROOT / "models" / "config.yaml").relative_to(REPO_ROOT)


def parse_args():
    parser = argparse.ArgumentParser(description="Upload models to CDF")
    parser.add_argument(
        "folders",
        type=str,
        nargs=1,
        help="The folders to monitor for deployment of data models",
    )
    parser.add_argument(
        "deploy_all",
        type=str,
        nargs="?",
        help="The folders/files to deploy to all",
        default=None,
    )
    return parser.parse_args()


def main():
    args = parse_args()
    check_folders = [Path(f.strip()) for f in args.folders[0].split(",")]
    if missing := [f for f in check_folders if not f.exists()]:
        print(f"Input: Folders, {missing}, do not exist")
        exit(1)

    monitor_models = {
        model
        for folder in check_folders
        for model in folder.glob("**/*.yaml")
        if model != CONFIG_FILE
    }
    print(f"Found {len(monitor_models)} models to monitor for deployment")

    deploy_all_folders = []
    if args.deploy_all:
        deploy_all_folders = [Path(f.strip()) for f in args.deploy_all.split(",")]
        print(f"Input: Folder/file (may force deploy all): {deploy_all_folders!r}")

    # Compare against previous commit under the assumption of squash-only merges:
    diff = subprocess.check_output(
        "git diff --name-only HEAD^ HEAD".split(), text=True
    ).split()
    changed_files = set(map(Path, diff))

    if deploy_all_folders and any(
        changed.is_relative_to(deploy_all)
        for changed, deploy_all in itertools.product(changed_files, deploy_all_folders)
    ):
        to_deploy = ["/".join(model_path.parts) for model_path in monitor_models]
        print(
            "Common folder has one or more changed file(s), will deploy all functions"
        )
    else:
        to_deploy = [
            "/".join(changed.parts)
            for changed in changed_files
            if changed in monitor_models
        ]

    if to_deploy:
        # Green color to make it easier to spot in the logs
        print(f"\033[92mTo be deployed: {to_deploy}\033[0m")
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
