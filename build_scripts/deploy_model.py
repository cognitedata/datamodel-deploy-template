import os
import argparse

from cognite.client import CogniteClient
from pathlib import Path
from cognite.client.data_classes.data_modeling import ContainerApply, DataModelApply
from cognite.client.exceptions import CogniteAPIError
from yaml import safe_load


def parse_args():
    parser = argparse.ArgumentParser(description="Deploy model to CDF")
    parser.add_argument(
        "model_path",
        type=str,
        nargs=1,
        help="The path to the yaml file with the model to deploy",
    )
    parser.add_argument(
        "--dry-run", action=argparse.BooleanOptionalAction, default=False
    )
    return parser.parse_args()


def main():
    client = CogniteClient.default_oauth_client_credentials(
        project=os.environ["CDF_PROJECT"],
        tenant_id=os.environ["TENANT_ID"],
        cdf_cluster=os.environ["CDF_CLUSTER"],
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
    )
    try:
        client.iam.token.inspect()
    except CogniteAPIError:
        print("Unable to authenticate with CDF. Please check your credentials.")
        exit(1)

    args = parse_args()
    model_path = Path(args.model_path[0])
    is_dry_run = args.dry_run
    if not model_path.exists():
        print(f"Input: File, {model_path}, does not exist")
        exit(1)

    model = safe_load(model_path.read_text())
    if containers_raw := model.get("containers"):
        containers = [ContainerApply.load(container) for container in containers_raw]
        print(f"Found {len(containers)} containers to deploy")
        if not is_dry_run:
            created = client.data_modeling.containers.apply(containers)
            print(f"Created {len(created)} containers")
        else:
            print("Dry run, not deploying containers")

    if data_model := model.get("data_model"):
        data_model = DataModelApply.load(data_model)
        print(
            f"Ready to deploy {data_model.name}, ({data_model.space}, {data_model.external_id})"
        )
        if not is_dry_run:
            created = client.data_modeling.data_models.apply(data_model)
            print(f"Created {created.name!r} data model")
        else:
            print(f"Dry run, not deploying data model: {data_model.name}")


if __name__ == "__main__":
    main()
