# sentence_embedding_API (SEMBED)
The sentence_embedding_API is an API endpoint for embedding input sentences in english to feature embeddings.

## Using the SEMBED API
The user can interact with the sentence_embedding_API through GET request. The following documents every path the user can use, a description of what it does, and the necessary method and headers to pass with the request.

All parameters must be passed in as JSON data.

## Request Paths

### get_embeddings
Get embeddings for the input sentence, as specified by the user.
- Parameters:
  - `sentence`: The input sentence to embed.
    -  Examples: "Anirudh rocks" , "Vikram movie is fantastic"
- Method: GET
- Headers: "Content-type: application/json"
- Returns: JSON
    - Embeddings can be parsed using the key `response["embeddings"]`

## How to run locally and test the API
Run the below commands in the same order by cd'ing into this directory
```shell
$ pip3 install pipenv
$ export PIPENV_VENV_IN_PROJECT=1
$ pipenv install
$ pipenv shell
$ python3 main.py
```
Test the API using the below command
```shell
$ curl -X POST -H "Content-type: application/json" -d '{"sentence": "Life is beautiful"}' http://localhost:5000/get_embeddings
```

## Requesting within the Kubernetes Cluster
All request URLs should be in the format: `http://<service-IP>:<service-port>/<request-path>`. You can get the IP and port of
the service by running `kubectl get svc sembed -n sembed` in the terminal.

- Example:
```shell
$ curl -X POST -H "Content-type: application/json" -d '{"sentence": "Life is beautiful"}' http://<svc-IP>:<svc-port>/get_embeddings
```
## Calling the API using Domain name
- `www.sembed.com` is only for reference
- `www.sembed.com/health_check` returns `{"status": "healthy"}`
- `www.sembed.com/get_embeddings` will return a JSON containing the embeddings

### How to test nginx ingress
If you are using [minikube](https://minikube.sigs.k8s.io/docs/start/) to deploy kubernetes cluster

Follow the below steps to test `www.sembed.com` from your local browser
In your Mac/Linux machine
```shell
$ sudo vim /etc/hosts
```
Add the below line and save
- `127.0.0.1  www.sembed.com`

Open a new terminal, run the below command and keep the terminal open
```shell
$ minikube tunnel
```
Call `www.sembed.com` from your browser to get the health check JSON

Pass `sentence` parameter in a JSON body in a POST request to get embeddings
