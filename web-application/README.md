# NOTE—Creating this infrastructure may incur costs. Please refer to the AWS pricing for more information.

:TODO: Provide an overview of the benefits of this project.

## Installation

#### Please note that since various services are being deployed, the AdministratorAccess would make it easy. However, we recommend deleting or disabling the user or removing the policy from the user upon deployment completion. You would only require access for deployment.

:TODO: AdministratorAccess policy is to be refined.

1.) AWS Account & Permissions: You'll need an AWS account and the IAM user permissions with the `AdministratorAccess` policy required

2.) Create an S3 bucket in your AWS account to store the Terraform-generated state file and the bucket name in GitHub secrets.

3.) GitHub Permissions: Generate the GitHub personal token under user profile https://github.com/settings/tokens

![alt text](https://github.com/sathia-s/aws-ivs-inspector/blob/main/prequisites/01-PersonalAccessToken-using-Classic.png?raw=true)

Assign the following permission and save.

![alt text](https://github.com/sathia-s/aws-ivs-inspector/blob/main/prequisites/02-AddFollowingPermissions.png?raw=true)

4.) Repository Workflow Permission:

![alt text](https://github.com/sathia-s/aws-ivs-inspector/blob/main/prequisites/05-ProvideWorkflowPermissions.png?raw=true)

5.) Create Environment:

![alt text](https://github.com/sathia-s/aws-ivs-inspector/blob/main/prequisites/03-AddNewEnvironment.png?raw=true)

6.) Manually set the GitHub Actions Secrets:
`AWS_ACCESS_KEY_ID`
`AWS_ACCOUNT_ID`
`AWS_S3_BUCKET_FOR_TF_STATE`
`AWS_SECRET_ACCESS_KEY`
`GH_PERSONAL_ACCESS_TOKEN`
`IVS_PROJECT_NAME`

![alt text](https://github.com/sathia-s/aws-ivs-inspector/blob/main/prequisites/04-AddSecerts.png?raw=true)

7.) Click the RunWorkflow for each workflow in sequence,

![alt text](https://github.com/sathia-s/aws-ivs-inspector/blob/main/prequisites/06-ClickTheRunWorkflowForEach.png?raw=true)

<<<<<<< HEAD:web-application/README.md
01:AWS Amplify App (source: 01-tf-amplify.yml)

> #### Note: If you're hosting the Web Application using Amplify to a desired region, you may update the value of `TF_VAR_region` in the workflow file `01-tf-amplify.yml` at `line #6`.

02:AWS Infra ap-south-1 (source: 02-tf-infra.yml)

> #### Note: If you're deploying infrastructure to another or additional region to inspect the IVS Channel resources, you may update the value of `TF_VAR_region` in the workflow file `02-tf-infra.yml` at the `line #6` for each run/region.

> 03:AWS IVS Inspector web-app (source: 03-awscli-web.yml)

> #### Note: Workflow `01-tf-amplify.yml` will automatically save the GitHub Actions Variable `AMPLIFY_APP_ID`, which is reused by another workflow `03-awscli-web.yml` for application deployment from GitHub using GitHub's `Personal Access Token`. Hence no action required adding the `AMPLIFY_APP_ID` in the environment variables.
=======
> 01:AWS Amplify App (source: 01-tf-amplify.yml)

#### Note: If you're hosting the Web Application using Amplify to a desired region, you may update the value of `TF_VAR_region` in the workflow file `01-tf-amplify.yml` at `line #6`.

> 02:AWS Infra ap-south-1 (source: 02-tf-infra.yml)

#### Note: If you're deploying infrastructure to another or additional region to inspect the IVS Channel resources, you may update the value of `TF_VAR_region` in the workflow file `02-tf-infra.yml` at the `line #6` for each run/region.

> 03:AWS IVS Inspector web-app (source: 03-awscli-web.yml)

#### Note: Workflow `01-tf-amplify.yml` will automatically save the GitHub Actions Variable `AMPLIFY_APP_ID`, which is reused by another workflow `03-awscli-web.yml` for application deployment from GitHub using GitHub's `Personal Access Token`. Hence no action required adding the `AMPLIFY_APP_ID` in the environment variables.
>>>>>>> refs/remotes/origin/dev:README.md

<!-- 8.) If you're hosting the Web Application using Amplify to a desired region, you may update the value of `TF_VAR_region` in the workflow file `01-tf-amplify.yml` at `line #6`. -->

<!-- 9.) If you're deploying infrastructure to another or additional region to inspect the IVS Channel resources, you may update the value of `TF_VAR_region` in the workflow file `02-tf-infra.yml` at the `line #6` for each run/region. -->

<!-- 10.) Workflow `01-tf-amplify.yml` will automatically save the GitHub Actions Variable `AMPLIFY_APP_ID`, which is reused by another workflow `03-awscli-web.yml` for application deployment from GitHub using GitHub's `Personal Access Token`. -->

## Renaming Project Name

The default project name, `ivs-inspector,` inherits from the repository/project. If you wish to change it, you may do so by changing the value of the secret variable `IVS_PROJECT_NAME` under the secrets tab found in the GitHub > Repository > `Settings` > `Secrets and variables` > `Actions`.

### Web Application Access

Upon successful run of all three workflows 01, 02, 03,

1. navigate to AWS Console,
2. switch to the region where the web application deployed,
3. select Amplify service,
4. select/enter the IVS Inspector App,
5. under overview > Production branch, click the Domain; thats is the URL of the IVS Inspector application.

:TODO: Provide details on how to use the web application.

:TODO: Question to the IVS team,

1. should we consider duplicating the #02 workflow for multiple region deployment or advise the customers to rename the region from the existing file. Please refer to #5 in the installation.

2. Should I decouple by moving the web application to a separate branch (say ivs) and keeping the Terraform folders and GitHub workflows in the main branch to avoid clutter and the branches specific to the behaviour?