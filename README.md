# datamodel-deploy-template
Template repository for deploying data models to CDF

Create an github environent (default name in the pipeline assumes `test`).
In the environment add the following variables:
- `COGNITE_TENANT_ID`
- `COGNITE_CLIENT_ID`
- `COGNITE_PROJECT`
- `COGNITE_CLUSTER` (api, westeurope-1, az-eastus-1 etc)

Add a secret named:
- `COGNITE_CLIENT_SECRET`

If you are using non AAD idP like AUTH0 or Keycloak, set the environment variables `COGNITE_TOKEN_URL` and `COGNITE_AUDIENCE` as well (`COGNITE_TENANT_ID` not needed). `deploy-push.yaml` also needs modifications to use these variables (uncomment 4 lines)


The `datamodels` folder contains one folder per datamodel. The name of the folder will be the name and externalid of the model. In the folder put a file named `datamodel.graphql` with the schema and a config file named `datamodel_config.yaml` where you can specify specific config for the model. Currently it's `version` and `space` to deploy to. You can also create a file named `datamodel_config_<environment>.yaml` to have environment specific configuration.

In the `datamodel.graphql` you can use the variables `$SPACE` and `$VERSION`, these will be replace by the `space` and `version` specifed in the `datamodel_config.yaml`
