## Deployment Pipeline

The deployment pipeline is controlled by the following two GitHub Actions workflows:

* [Generate Model Deployment Matrix](workflows/generate-matrix.yaml) - Figures out which models to deploy based on 
  the `git` diff between the current and previous commit. The matrix is then used to trigger the next workflow.
* [Publish data model](workflows/deploy-push.yaml) - This is run on each model determined by the Generate 
  Model Deployment Matrix workflow. This workflow will deploy the model to the CDF environment specified in the
  GitHub environment.

The following Python scripts are used by the workflows above to deploy the models:

* [Changed Models](../build_scripts/changed_models.py) - Determines which models have changed between the current and 
  previous commit.
* [Replace Vars](../build_scripts/replace_vars.py) - Updates the model files with the variables set in
  the [config.yaml](../models/config.yaml) file.
* [Deploy Model](../build_scripts/deploy_model.py) - Deploys the model to the CDF environment specified in the 
  GitHub environment.

