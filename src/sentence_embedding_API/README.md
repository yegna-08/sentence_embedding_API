# sentence_embedding_API
The sentence_embedding_API is an API endpoint for embedding input sentences in english to feature embeddings.

## Using the API
The user can interact with the sentence_embedding_API through GET request. The following documents every path the user can use, a description of what it does, and the necessary method and headers to pass with the request.

All parameters must be passed in as JSON data.

## Requesting within the Kubernetes Cluster
All request URLs should be in the format: `http://<service-IP>:<service-port>/<request-path>`. You can get the IP and port of
the service by running `kubectl get svc sembed -n sembed` in the terminal.

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
- Example: `curl -X GET -H "Content-type: application/json" -d '{"sentence": "Life is beautiful"}' http://<svc-IP>:<svc-port>/get_embeddings`

