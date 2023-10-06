import argparse
from pathlib import Path
from yaml import safe_load

REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = (REPO_ROOT / "models" / "config.yaml").relative_to(REPO_ROOT)


def parse_args():
    parser = argparse.ArgumentParser(description="Update the space variables in files")
    parser.add_argument(
        "model_path",
        type=str,
        nargs=1,
        help="The path to the yaml file with the model to deploy",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    model_path = Path(args.model_path[0])
    if not model_path.exists() or model_path.suffix != ".yaml":
        print(f"Input: File, {model_path}, does not exist or is not a yaml file")
        exit(1)

    config = safe_load(CONFIG_FILE.read_text())
    if not (values_by_variable := config.get("variables")):
        print("No space variables to update")
        exit(0)

    print(
        f"Updating the following variables {','.join(f'{value}={key}' for key, value in values_by_variable.items())}"
    )
    print(f"Updating {model_path}")
    model_text = model_path.read_text()
    for key, value in values_by_variable.items():
        model_text = model_text.replace(value, key)
    model_path.write_text(model_text)


if __name__ == "__main__":
    main()
