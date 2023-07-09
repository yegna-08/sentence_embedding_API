# sentence_embedding_API (SEMBED)
API that gets a sentence in english as input and returns embeddings as array of floats

## Table of Contents
- [Project Tree Structure](#project-tree-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Nginx](#nginx)
    - [Host Names](#host-names)
  - [Install SEMBED API](#install-sembed-api)
- [Upgrading](#upgrading-sembed)
- [Clean Up](#clean-up)
- [Quickstart](./src/sentence_embedding_API/README.md)
- [Unit Testing](./tests/README.md)

## Project tree structure

- __sentence\_embedding\_API__
   - [LICENSE](LICENSE)
   - [README.md](README.md)
   - __deploy__
     - __sembed__
       - [Chart.yaml](deploy/sembed/Chart.yaml)
       - __charts__
       - __templates__
         - [NOTES.txt](deploy/sembed/templates/NOTES.txt)
         - [\_helpers.tpl](deploy/sembed/templates/_helpers.tpl)
         - [configmap.yml](deploy/sembed/templates/configmap.yml)
         - [deployment.yaml](deploy/sembed/templates/deployment.yaml)
         - [hpa.yaml](deploy/sembed/templates/hpa.yaml)
         - [ingress.yaml](deploy/sembed/templates/ingress.yaml)
         - [service.yaml](deploy/sembed/templates/service.yaml)
         - [serviceaccount.yaml](deploy/sembed/templates/serviceaccount.yaml)
       - [values.yaml](deploy/sembed/values.yaml)
   - __src__
     - __sentence\_embedding\_API__
       - [Dockerfile](src/sentence_embedding_API/Dockerfile)
       - [Pipfile](src/sentence_embedding_API/Pipfile) # For package dependency management
       - [Pipfile.lock](src/sentence_embedding_API/Pipfile.lock)
       - [README.md](src/sentence_embedding_API/README.md) # Contains API documentation
       - __config__
         - [config.cfg](src/sentence_embedding_API/config/config.cfg) # for local testing, in the production we use kubernetes configmap
       - [logger.json](src/sentence_embedding_API/logger.json)
       - [main.py](src/sentence_embedding_API/main.py) # Actual code that embeds the input sentence
       - [requirements.txt](src/sentence_embedding_API/requirements.txt)
       - [requirements\_raw.txt](src/sentence_embedding_API/requirements_raw.txt) # for pipenv usage
   - __tests__
     - [README.md](tests/README.md) # Contains Unit Testing documentation
     - [\_\_init\_\_.py](tests/__init__.py)
     - [requirements.txt](tests/requirements.txt) # Contains Unit Testing dependencies
     - __sentence\_embedding\_API__
       - [\_\_init\_\_.py](tests/sentence_embedding_API/__init__.py)
       - [test\_main.py](tests/sentence_embedding_API/test_main.py)
   - [tox.ini](tox.ini) # Automate Unit Testing build and run


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
