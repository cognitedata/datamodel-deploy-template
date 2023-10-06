import os
import argparse

from cognite.client import CogniteClient
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Deploy Models to CDF")
    parser.add_argument()


def main():
    client = CogniteClient.default_oauth_client_credentials(
        project=os.environ["CDF_PROJECT"],
        cdf_cluster=os.environ["CDF_CLUSTER"],
        tenant_id=os.environ["TENANT_ID"],
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        token_url=os.environ["TOKEN_URL"],
    )

    client.data_modeling.containers.apply()


if __name__ == "__main__":
    main()
