# Elgo Anomaly

#### Step 1: Clone repo and configure environment

If you have not done so, configure your AWS CLI with a profile linked to your account.

```
aws configure --profile ANY_NAME_YOU_LIKE
```

Next, please clone this repo onto any PATH onto your machine.

```
git clone CURRENT_REPO
cd
```

Once you successfully cloned this repo, please edit deploy.env file to replace <ANY_NAME_YOU_LIKE> to the profile name you just created above. You can also edit AWS_REGION and ENVIRONMENT. Run the following command after you have modified deploy.env with your aws profile name:

```
source deploy.env
```

Then, we are going to use the contents in provisioning_cf_script folder.

```
cd cloud_formation
```

### Step 2: Understand deploy.sh script

Examine the deploy.sh file. This is the starting point of the cloud formation.
This bash script first creates a S3 bucket to store all of the relevant assets created in this repo. Then, it
calls `template.yaml` CloudFormation script with AWS SAM CLI toolset.

### Step 3: Run deployment of cloud resources

Run the provisioning script:

```
. deploy.sh
```

After CloudFormation runs successfully, the cloud resources all the way to Sagemaker should be created.
