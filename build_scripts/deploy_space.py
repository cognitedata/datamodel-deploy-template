import argparse, os

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes.data_modeling import SpaceApply

def parse_args():
    parser = argparse.ArgumentParser(description="Create datamodel space if needed")
    parser.add_argument("--space", type=str, nargs="?", help="Name of space", default=None)
    return parser.parse_args()


def get_cognite_client():

    if "COGNITE_TENANT_ID" in os.environ:
        token_url = f"https://login.microsoftonline.com/{os.environ['COGNITE_TENANT_ID']}/oauth2/v2.0/token"
    else:
        token_url = os.environ["COGNITE_TOKEN_URL"]

    if "COGNITE_SCOPES" in os.environ:
        scopes = os.environ['COGNITE_SCOPES']
    else:
        scopes = f"https://{os.environ['COGNITE_CLUSTER']}.cognitedata.com/.default"


    oauth_provider = OAuthClientCredentials(
        token_url=token_url,
        client_id=os.environ["COGNITE_CLIENT_ID"],
        client_secret=os.environ["COGNITE_CLIENT_SECRET"],
        scopes=[scopes],
        #Any additional IDP-specific token args. e.g.
        audience=os.environ.get("COGNITE_AUDIENCE", None),
    )

    cnf = ClientConfig(
        client_name="datamodel-deploy",
        project=os.environ["COGNITE_PROJECT"],
        credentials=oauth_provider,
        base_url=f"https://{os.environ['COGNITE_CLUSTER']}.cognitedata.com",
        debug=False
    )

    return CogniteClient(config=cnf)


def main():
    args = parse_args()
    client = get_cognite_client()

    space = args.space

    if not client.data_modeling.spaces.retrieve(space=space):
        print(f"Space {space} does not exist, creating.")
        spaces = [SpaceApply(space=space, description=space, name=space)]
        client.data_modeling.spaces.apply(spaces)

if __name__ == "__main__":
    main()
