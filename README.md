# Kubeflow Assignment

## Install Kubernetes Cluster (MiniKube single node deployment)

1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)

```bash 
sudo apt-get update
sudo apt-get -y install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 
```

2. [Install MiniKube](https://minikube.sigs.k8s.io/docs/start/) and create K8s cluster

```bash 
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```

3. [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Deploy Kubeflow Pipelines

1. [Deploy Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/) to K8s cluster

```bash 
export PIPELINE_VERSION=1.8.1
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

2. Verify that the Kubeflow Pipelines UI is accessible by port-forwarding:

```bash 
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80 --address=0.0.0.0
```

3. Access Kubeflow UI

```bash
curl http://localhost:8080/
curl http://172.31.7.162:8080/ # private network
curl http://18.132.68.212:8080/ # public network
```

To access URL via public network, edit the VM's assigned security groups to enable Inbound Traffic TCP traffic to port 8080. 

## MinIO File Storage

[x] Write manifest for stateful MinIO app
[ ] Write python client for 2nd stage app

## Create PVC

[ ] Check altnerative PVC backends (work with exisiting local file PVs?)

## Create file-collect Container

1. [Component development](https://www.kubeflow.org/docs/components/pipelines/sdk/component-development/#design)

2. Run app directly (testing)

```bash
python3 file-collect/file-collect.py --user "DanielSCrouch" --repo "safe-intel" --branch "main" --subdirectory "files" --outdir "/tmp/tmp" --respath "/tmp/results"
```

3. Build containerised applications 

```bash 
cd hack
./build-images.sh
```

3. Run app via Docker

```bash
docker run \
  -e USER='DanielSCrouch' \
  -e REPO='safe-intel' \
  -e BRANCH='main' \
  -e SUBDIRECTORY='files' \
  -e OUTDIR='/tmp/tmp' \
  -e RESPATH='/tmp/results' \
  duartcs/filecollect:latest
```

## Create file-copy Container

[ ] Consume same PCV as stage 1
[ ] Write app to receive list of file paths as inputs 
[ ] Write Minio client to upload files to local cloud storage (or S3?)

## Create Pipeline 

1. [Install the Kubeflow Pipelines SDK](https://www.kubeflow.org/docs/components/pipelines/sdk/install-sdk/)

```bash 
python3 -m venv venv
source venv/bin/activate
pip3 install kfp --upgrade
```

## Requirements

```bash 
pip3 freeze > requirements.txt
pip3 install -r requirements.txt
```
