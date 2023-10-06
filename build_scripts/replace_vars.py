import argparse
from pathlib import Path
from yaml import safe_load

REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = (REPO_ROOT / "models" / "config.yaml").relative_to(REPO_ROOT)


def parse_args():
    parser = argparse.ArgumentParser(description="Update the space variables in files")
    parser.add_argument(
        "folders",
        type=str,
        nargs=1,
        help="The folders to monitor for deployment of data models",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    check_folders = [Path(f.strip()) for f in args.folders[0].split(",")]
    if missing := [f for f in check_folders if not f.exists()]:
        print(f"Input: Folders, {missing}, do not exist")
        exit(1)
    monitor_models = [
        model
        for folder in check_folders
        for model in folder.glob("**/*.yaml")
        if model != CONFIG_FILE
    ]
    config = safe_load(CONFIG_FILE.read_text())
    if not (space_by_variable := config.get("spaces")):
        print("No space variables to update")
        exit(0)

    print(
        f"Updating the following space variables {','.join(f'{value}={key}' for key, value in space_by_variable.items())}"
    )
    for model in monitor_models:
        print(f"Updating {model}")
        model_text = model.read_text()
        for key, value in space_by_variable.items():
            model_text = model_text.replace(value, key)
        model.write_text(model_text)


if __name__ == "__main__":
    main()
