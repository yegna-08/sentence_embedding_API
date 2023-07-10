# This document contains design justification on why the API is in production quality

To make the sentence embedding API ideal for production I have enhanced scalability, observability, load balancing, API security, automated unit testing, continuous integration and deployment, release management, and efficient containerization of the application.

- Used `FastAPI` framework for developing the API
    - Has input validation
    - Logging every input and response
    - Requires the incoming request to contain only JSON body
    - package dependency maintained using `pipenv`
- Unit Testing using `Pytest`
    - Ensures each statement in the API behaves as expected, validating inputs, outputs, and corner cases - Helps identify and address potential bugs or issues, improving the overall robustness of your API
    - Included coverage report to find the missing statements that requires testing
    - Automated unit testing build and run using `tox`
- Containerized the API and deploy in `Kubernetes` as Microservice
    - Auto Scalability using Horizontal pod autoscaler
    - Availability by setting number of replicas to 3
    - Health checks using liveness and readiness probe
    - Extensibility as the same infrastructure can be used to deploy multiple APIs
    - Release software with greater speed and frequency
    - Cross-cloud portability
- `Istio` for networking and security for the application
    - Seperate business logic from security and networking logic using Istio
    - Production requires robust security such as JSON Web Tokens (JWT), rate limiting
    - `Envoy` proxy which is Layer 4 and 7 Load Balancer
    - Authorization policy to allow only defined traffic routes and only from certain namespaces
    - Observability, allowing you to collect and analyze detailed metrics, logs, and traces for monitoring and debugging purposes
- `Nginx` as an alternate to istio
    - Load balancing
    - Rate limiting functionality
- Continuous integration and Continuous Delivery using `GitHub Actions`
    - Three workflows to automate testing, creating new release and containerizing the application
    - Tagged releases and versioned `Helm charts` for better maintenance
