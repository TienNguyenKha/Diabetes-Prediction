# MLE practice - Diabetes Prediction model

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

* Contents:
    * [Introduction](#introduction)
    * [System architecture](#system-architecture)
	* [Prerequisites installation](#prerequisites-installation)
	* [Component Preparation](#component-preparation)
	* [Additional Usage](#additional-usage)
	* [TODOs](#todos)
<!-- /code_chunk_output -->

## Introduction:
This is the project when I first learned about MLE. This repo will help and guide you to build and serve ML model as in a production environment (Google Cloud Platform). I also used tool & technologies to quickly deploy the ML system into production and automate processes during the development and deployment of the ML system.

## System architecture:

![systempipline](assets/systempipeline.png)

* Source control: Git/Github
* CI/CD: Jenkins
* Experiment tracking & Model registry: MLflow
* Build API: FastAPI
* Containerize application: Docker
* Container orchestration system: Kubernetes/K8S

### Kubernetes architecture:
![k8sarchi](assets/Kubernetesarchi.png)

## Prerequisites installation:
### Google Cloud Platform: Account Registration & Project Billing
Google Cloud Platform will be the cloud we use in this project, so you should access https://console.cloud.google.com/ and register an account. (If you have a Gmail account, this should be easy)

After creating GCP account, let's create your own `Project` now:
![CreatenewproGCP](assets/CreatenewProjectGCP.png)

Fill Project name (for example, "mlecourse" ), and hit **Create**
![CreatenewproGCP2](assets/CreateNewprojectGCP2.png)

**Note**: Remember to create a `billing account` after creating the project, then linking that `billing account` to the newly created project (refer: [Create and Link Billing account](https://www.youtube.com/watch?v=uINleRduCWM) ). If you've never used GCP before, choose "START MY FREE TRIAL" to try it out for 3 months for free.

Next, navigate to [Compute Engine API UI](https://console.cloud.google.com/marketplace/product/google/compute.googleapis.com) to "ENABLE" **Compute Engine API**:
![EnableComputeEngine](assets/EnableComputeEngineAPI.png)

Navigate to [Kubernetes Engine API UI](https://console.cloud.google.com/marketplace/product/google/container.googleapis.com) to "ENABLE" **Kubernetes Engine API**
![Enablek8s](assets/enableK8s.png)


### Install the gcloud CLI:
We can easily connect to GKE using the Gcloud CLI. Reading this guide to install gcloud CLI in local terminal [gcloud CLI](https://cloud.google.com/sdk/docs/install#deb).


After that, initialize the gcloud CLI by typing `gcloud init`, then type "Y"
```bash
gcloud init
```
**Note**:
* A pop-up to select your Google account will appear, select the one you used to register GCP, and click the button Allow
* Now, go back to your terminal, in which you typed `gcloud init`, choose your project, and Enter.
*  Then type Y, and select the area that is ideal for you., then Enter.
### Install dev environment:
#### Requirements:

```bash
pip install -r requirements_dev.txt
```

**Note**: Simply said, this is the setting when you code locally. The `requirements.txt` file specifies the application environment in detail.

### Additional Installation (Skip if you have already installed):
* [Docker](https://docs.docker.com/desktop/install/ubuntu/)
* [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
* [kubectx + kubens](https://github.com/ahmetb/kubectx#manual-installation-macos-and-linux) (Optional)
* [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli#install-terraform)

## Component Preparation:

### Create Jenkins on google cloud VM:

Let's create your Jenkins VM instance using `ansible`.

Before creating google cloud VM by ansbile, you must first prepare a few things to access the GCP like `service account`. You can refer to this link [Create service account](https://cloud.google.com/iam/docs/service-accounts-create)

**Note**: When creating a service account, grant it `Compute admin` permission. And then:

* Find the three dots icon in the service account's Actions column, then select Manage keys.
* Click ADD KEY, then Create new key
* Download a JSON file by selecting CREATE. Keep this file SAFE at all times.
* Put your credentials under the folder `/local/ansible/secrets`

Create Jenkins VM instance on GCP.
```bash
cd /local/ansible/deploy_jenkins
ansible-playbook create_compute_instance.yaml
```

**Note**:Please check the file `create_compute_instance.yaml`. The `project id` and `service account` should be changed to match yours (e.g., line 11 & line 14, line 43 & line 45).

After creating your Jenkins VM instance on GCP, navigate to [VM instance UI](https://console.cloud.google.com/compute/instances) and COPY `external IP` corresponding with yours. I COPY `external IP` "jenkins-instance" for example:

![ansibleIP](assets/AnsibleIP.png)

Modify the IP of the newly created instance to the `inventory` file, then run the following commands:
```bash
ansible-playbook -i ../inventory deploy_jenkins.yml
```

<!-- Integrate your github source to the Jenkins VM once it has been created. You can follow this link: [Integrate Jenkins with GitHub ](https://www.whizlabs.com/blog/integrate-jenkins-with-github/) -->
#### Add SSH key:
First, check if we can connect to the External IP via port 22 by using telnet on your local terminal:
```bash
telnel <jenkins_external_IP> 22
```

We will see a notification that you have successfully connected if you did it correctly

Generate your SSH key first. Open your local terminal, type `ssh-keygen` and type Enter to die until Overwrite:
```bash
ssh-keygen
```

Navigate to [METADATA](https://console.cloud.google.com/compute/metadata) and Select the tab SSH KEYS and click the button + ADD ITEM (or ADD SSH KEY if you don’t see the + ADD ITEM button):

Copy the content of your file `~/.ssh/id_rsa.pub` to GCP and press the blue button SAVE at the bottom of the page:


![sshkey](assets/sshkeyy.png)

**Note**: To see the content of the file `~/.ssh/id_rsa.pub`, use the cat command
```bash
cat ~/.ssh/id_rsa.pub
```

### Create GKE cluster:

Change directory to `/terraform` folder and initializes a working directory containing Terraform configuration files.
```bash
cd /terraform
terraform init
```
Then you can creates an execution plan, which lets you preview the changes that Terraform plans to make to your infrastructure.

```bash
terraform plan
```

Note: Before creates an execution plan, you should authenticate with GCP first using the following command:

```bash
gcloud auth application-default login
```

Carries out the planned changes to each resource using the relevant infrastructure provider's API.

**Note**: It will ask you for confirmation before making any changes. Type `yes` if you have checked the execution plan carefully.

```bash
terraform apply
```

### Connect to the GKE cluster:

After `terraform apply` successfully, you have now initialized the gke cluster. Let's install [Helm](https://helm.sh/docs/intro/install/) to deploy application on the k8s cluster easily.

Then navigate to [GKE UI](https://console.cloud.google.com/kubernetes):

![GKEui](assets/GKEui.png)

Click on the cluster "mlecourse-399310-gke" for example and select "CONNECT"
![GKEconnect0](assets/GKEconnect0.png)

A pop-up to CONNECT to your cluster will appear:

![GKEconnect](assets/GKEconnect.png)

Copy the line "gcloud container ..." into your local terminal:
```bash
gcloud container clusters get-credentials <your_gke_name> --zone us-central1-c --project <your_project_id>
```
We should see the line "kubeconfig entry generated for mlecourse-399310-gke" after above command.

Then, switch to your gke cluster using kubectx:
```bash
kubectx <YOUR_GKE_CLUSTER>
```

Install the `nginx controller` on this new cluster right now to route traffic from outside to services within the cluster.

```bash
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```

<!-- **Note**: Remember to create a namespace `model-serving` first in your new cluster. Because our application will be deployed in `model-serving` namespace.
```bash
kubectl create ns model-serving
``` -->

### Create Prometheus and Grafana monitoring:
Prometheus and Grafana form a powerful combination for monitoring and observability. Therefore, I will utilize these two tools as my cluster's monitoring services.

Change directory to /`prometheus-grafana` folder and using helm to install Prometheus and Grafana on newly created cluster:
```bash
cd /prometheus-grafana
helm upgrade --install prometheus-grafana-stack -f values-prometheus.yaml kube-prometheus-stack --namespace monitoring --create-namespace
```
**Note:** View more information and get additional guide at [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)

Now both prometheus and grafana have been installed on GKE cluster (in namespace `monitoring`).

Let's verify each matching monitoring service's host name and ingress IP to see if it has been installed successfully or not:
```bash
kubectl get ingress -n monitoring
```
We should see our Ingresses after this command.
If you see host names for ingress like "grafana.tiennk.com," "alertmanager.tiennk.com" and "prometheus.tiennk.com" for example, with their corresponding addresses. That indicates that the installation was successful.

So we are going to do now is that we are going to take that addresses and in our `etc/hosts` file.

```bash
sudo vi /etc/hosts
```

At the end of open file (below example image), we gonna define our mapping.
![IPmapping](assets/mappingIPP.png)

 And this works locally if we are going type "prometheus.tiennk.com" in the browser (below image example), and this will be the IP address that it's going to be mapped to. Do the same way when visiting "alertmanager.tiennk.com" or "prometheus.tiennk.com"
 ![prometheusUIexample](assets/prometheusUIexample.png)

**Note**: The domain names of the monitoring services can be altered to suit your preferences. To set them up, open the values-Prometheus.yaml file. Lines `364` for Alertmanager, `919` for Grafana, and `2726` for Prometheus are in particular.

#### Sending Prometheus Alerts to Discord with Alertmanager:

First, create an alerting rule with `additionalPrometheusRules` in `values-prometheus.yaml` file (line 154). You could also simply use the rule I've already built to stay an eye on Node memory.

Setting up a webhook on `Discord`:

I assume you're already using Discord and have a channel that you want to send alerts to (in this example, we're using #alerts).

Edit the channel settings by clicking the "Edit Channel" cog button:
![discordWebhook](assets/webhookdiscord.png)

Next, head to the "Integrations" menu item:

![Intergrate](assets/discordIntergrate.png)

Click on "Create Webhook":
![CreateWebhook](assets/createWebhook.png)

Click on the newly added hook:
![newlyCreateWebhook](assets/newlyCreatedwebhook.png)

Adjust the name, copy the webhook URL, and save the hook:

![Botconfig](assets/Botdiscordconfig.png)

Then go to line 297 in `values-prometheus.yaml` file to replace the <DISCORD_WEBHOOK_URL> placeholder with the webhook URL you just copied from Discord. It should look something like this: https://discord.com/api/webhooks/XXX/YYY.

The config above will sends all alerts (grouped by alertname and job) to a single Discord receiver.

### CI/CD with Jenkins:

First, ssh to your new jenkins VM again:
```bash
ssh -i ~/.ssh/id_rsa username@jenkins_externalIP
```

Check if `jenkins` container is running:
```bash
sudo docker ps
```
![Jenkinscheck](assets/jenkincheck.png)

Ok! jenkins is running successfully. Let get the jenkins password now:
```bash
sudo docker exec -ti jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open web browser jenkins UI through http://yourExternalIP:8081/ and paste jenkins password:

![Jenkinslogin](assets/loginjenkins.png)

After entering the password, install the "set sugested plugin". And information for the user can be next/skiped and so on ...


Now, you are in Jenkin UI:

![JenkinsUI](assets/jenkinsUI.png)

Then navigate to Dashboard > Manage Jenkins > Plugins > Available plugin. And SELECT Docker, Docker pipeline, gcloud SDK, kubernetes. Then SELECT "Install without restart" or "Download now and install after restart"

And then you can create new Jenkins pipeline by following these step:
* Click the New Item menu within Jenkins Classic UI left column

* Provide a name for your new item (e.g. My-Pipeline) and select Multibranch Pipeline

* Click the Add Source button, choose the type of repository you want to use and fill in the details

* Click the Save button and watch your first Pipeline run.

**Note**: Remember to connect and assign permissions so that Jenkins may connect to the K8s cluster.
## Additional Usage:
### Mlflow deploy:
In case you want EDA and training model from my notebooks. You need deploy MLflow up by following command:
```bash
pip install mlflow==2.6.0
docker compose -f ./ops_platform/mlflow/mlflow-docker-compose.yml up -d
```
Then you can open MLflow's web browser through: http://localhost:5000/

![Mlflow](assets/Mlflow.png)

Now, you can do Experiment tracking & Model registry more easier with MLflow.

### Pre-commit:
If you want to inspect the snapshot that's about to be committed, to see if you've forgotten something, to make sure tests run, or to examine whatever you need to inspect in the code. Let's use `pre-commit`
```bash
pip install pre-commit
pre-commit install #After the installation is complete, from that moment on, if there is a new commit, the pre-commit guy will help us format the code.
pre-commit run --all-files # run all files
```

### Yamlint:
This tool to check your `yaml` file in your repo:
```bash
pip install yamllint
yamllint <yaml_file_name>.yaml
```

## TODOs
 + Building observability system on kubernetes (Prometheus and grafana)
