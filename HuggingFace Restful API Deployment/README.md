# Model Deployment via Azure Kubernete Service
### What does the application do?
The application in the 'main.py' file provides a FastAPI service using uvicorn (as async webworker), featuring multiple endpoints. Pydantic models are employed to define and validate the structure of request and response bodies for the /project-predict and /health endpoints. The application leverages Redis as a caching backend, ensuring efficient data retrieval for common queries and predictions. Below are the four primary custom made endpoints:

* **/health** endpoint
    + **input**: None required.
    + **output**: Return the current time in UTC format. 

* **'/project-predict'** endpoint: Predicts the sentiments of input setences using a fined-tuned Bert model on this Huggingface repo called [`distilbert-base-uncased-finetuned-sst2`](https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2).
    + **Input:** A set of sentence input  in JSON format. Below is a sample input format:<br/>
    ``{"text": ["example 1", "example 2"]}``
    + **Output:** A nested list containing the predicted positive and negative sentiment score for each input sentence. 
    ``{"predictions": [[{"label": "POSITIVE", "score": 0.7127904295921326}, {"label": "NEGATIVE", "score": 0.2872096002101898 }], [{"label": "POSITIVE", "score": 0.7186233401298523}, {"label": "NEGATIVE", "score": 0.2813767194747925 }]]}``

### How to build, deploy, and run the application on local Minikube
It is a good practice to test and deploy the application locally on Minikube via Docker. On local computer, the application is constructed based on commands and information provided within the Dockerfile. This Dockerfile guides the creation of a Docker image using the command: ``docker build -t my-api .``, where ``my-api`` is the name of the docker image. Once the docker image is built, can we use the Kubenete commands below to create namename, deployment, and service:
```bash
kubectl apply -f infra/namespace.yaml
kubectl config set-context --current --namespace=w255

kubectl get pods -n w255
kubectl get svc -n w255

kubectl apply -f infra/deployment-redis.yaml
kubectl apply -f infra/deployment-pythonapi.yaml
kubectl apply -f infra/service-prediction.yaml
kubectl apply -f infra/service-redis.yaml
```
The yaml file that that configure the application and redis deployment/service is located inside in this path `\mlapi\infra`.

The application is encapsulated within a Docker container and is seamlessly managed via Kubernetes using Minikube. To initiate the application, simply execute the `minikube.sh` script from the  root directory using the ``./minikube.sh`` command. <br/><br/>
Note: This script streamlines several operations: it starts Minikube, sets up the required Poetry environment, deploy it, and test its endpoints. Additionally, the script configures Docker to function within Minikube's environment, setup/configured w255 namespace, and leverages Kubernetes to adeptly deploy and oversee the application and its linked services.

### How to build and deploy the application
The application is built using commands and information specified in the Dockerfile. This file directs the creation of a Docker image using the command: ``docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .``, where ``IMAGE_NAME=project`` and TAG is the Git commit hash ID. This particular ``docker build`` command specifies the CPU architecture, ensuring compatibility with the Kubernetes cluster on Azure. This step is specifically necessary for systems with Apple Silicon architecture. After building the docker image, it is tagged with a specific format: ``w255mids.azurecr.io/mamesael/project:[TAG]``. Subsequently, the Docker image is pushed to the Azure repository for deployment and servicing. The following commands illustrate the sequence in which the application is built and deployed:

```bash
docker build --platform linux/amd64 -t project:[TAG] .
docker tag project:[TAG] w255mids.azurecr.io/mamesael/project:[TAG]
docker push w255mids.azurecr.io/mamesael/project:[TAG]
```
The ``build-script.sh`` script automates the above steps. It continuously updates the TAG in the Docker image name and in the patch-deployment-project.yaml file. This ensures that each build reflects the latest source code changes and maintains a consistent tagging system for deployment.

The application is containerized using Docker and managed through Kubernetes, specifically within the Microsoft Azure environment. Once the Docker image is successfully pushed to the Azure repository, Kubernetes is used for the deployment process. This is done using kubectl, the command-line tool for Kubernetes. To deploy the application in the production environment, the following commands are used:

```bash
kubectl kustomize .k8s/overlays/prod
kubectl apply -k .k8s/overlays/prod
```
The ``AKS.sh`` script automate the log-in, authentication, creating a specific docker name format, deploy the application, and test all the endpoints.

### How to Test the Application
The `test_mlapi.py` file is located at `..\mlapi\tests\test_mlapi.py` and contains unit tests using FastAPI's TestClient. These tests cover various edge cases for inputs, ranging from incorrect values, formats, and non-string inputs. To execute all the test cases in `test_mlapi.py`, use the command `poetry run pytest` in the `mlapi` directory.

These tests also utilize FastAPI's caching, which uses the InMemoryBackend for temporary data storage during the execution of each test case. This negates the need for an external caching system like Redis.


