# sentence_embedding_API (SEMBED)
API that gets a sentence in english as input and returns embeddings as array of floats

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Nginx](#nginx)
    - [Host Names](#host-names)
  - [Install SEMBED API](#install-sembed-api)
- [Upgrading](#upgrading-sembed)
- [Clean Up](#clean-up)
- [Quickstart](./src/sentence_embedding_API/README.md)
- [Unit Testing](./tests/README.md)

sentence_embedding_API
├── .github
│   ├── workflows
│   │   ├── docker.yml # builds and pushes the docker image
│   │   ├── release.ym  # creates a new release
│   │   ├── tests.yml # runs unit testing
├── src
│   ├── sentence_embedding_API
│   │   ├── config
│   │   |   ├── config.cfg # for local testing, in the production we use kubernetes configmap
│   │   └── .dockerignore
│   │   └── Dockerfile
│   │   └── logger.json
│   │   └── main.py # Actual code that embeds the input sentence
│   │   └── pipfile # For package dependency management
│   │   └── pipfile.lock
│   │   └── README.md  # Contains API documentation
│   │   └── requirements_raw.txt # for pipenv usage
│   │   └── requirements.txt
├── deploy
│   └── helm_chart
│   │   ├── sentence_embedding_API
│   │   │   └── templates
│   │   │       ├── configmap.yml
│   │   │       ├── deployment.yml
│   │   │       ├── hpa.yml
│   │   │       ├── ingress.yml
│   │   │       ├── service.yml
│   │   │       ├── serviceaccount.yml
│   │   │   └── Chart.yaml
│   │   │   └── values.yaml
├── tests/
│   ├── sentence_embedding_API
│   │   └── test_main.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── README.md # Contains Unit Testing documentation
│   ├── requirements.txt # Contains Unit Testing dependencies
├── .gitignore
├── tox.ini # Automate Unit Testing build and run
├── README.md


## Prerequisites
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- An existing Kubernetes cluster
  - Version 1.18+ is recommended for Nginx ingress controller to work
- [Helm](https://helm.sh/docs/intro/install/) version 3+

## Nginx
[Nginx](https://kubernetes.github.io/ingress-nginx/)
-  Add the repo
    - `helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx`
- Install ingress-nginx controller (Version 3.x.x for K8s version <=1.18, 4.x.x for v >= 1.19  )
    - `helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --create-namespace`
- No need to modify deploy/sembed/values.yaml

### Host Names
The existing values are only for reference
- `ingress.hosts.host: www.sembed.com`

Update helm repositories
- `helm repo update`

Lint the helm chart
- `helm lint ./sembed`

## Install SEMBED API
  - `helm install sembed ./sembed --namespace sembed --create-namespace`

## Upgrading SEMBED
To upgrade an existing SEMBED application
- `helm upgrade sembed ./sembed --namespace sembed`

## Clean Up
To uninstall SEMBED
- `helm delete sembed --namespace sembed`
