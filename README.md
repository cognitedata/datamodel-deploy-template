# datamodel-deploy-template
Template repository for deploying data models to CDF

## Setup Environments (e.g. dev, test, prod)
Create a GitHub environment (default name in the pipeline assumes `test`).
In the environment, add the following variables:
- `TENANT_ID`
- `CLIENT_ID`
- `CDF_PROJECT`
- `CDF_CLUSTER` (api, westeurope-1, az-eastus-1 etc)

Add a secret named:
- `CLIENT_SECRET`

## Setup Models
All models are kept in the `models` folder which has the following structure:
```
    📦models
     ┣ 📂information - Models described as containers. These models are for how the data is stored.
     ┣ 📂solution - Models described as data models (group of views). These models are for the end-user.
     ┗ 📜config.yaml - Variables for the models.
```

All models are assumed to be written as a `yaml` file. 

## Deployment Pipeline

See [deployment pipeline](.github/README.md) for more information on the deployment pipeline.
