cd mlapi

echo "1. Start up Minikube..."
minikube start --kubernetes-version=v1.27.3

echo "2. Setup docker daemon to built with Minikube"
eval $(minikube docker-env)

poetry install 

echo "Running pytest.."
poetry run pytest -vv

echo "3. Ensure API model is trained..."
if [ -e "./model_pipeline.pkl" ]; then
    echo " Model is available."
else
    echo "Training Model..."
    python ./trainer/trainer.py
fi

echo "4. Building the docker container..."
docker build -t my-api .
#docker build --no-cache -t my-api .
#docker build -t my-api -f mlapi/Dockerfile .
# docker run -d -p 8000:8000 --name apiContainer my-api


echo "5. Applying w255 name space."
kubectl apply -f infra/namespace.yaml
kubectl config set-context --current --namespace=w255

echo "6. Apply Deployments and Services:"
kubectl apply -f infra/deployment-redis.yaml
kubectl apply -f infra/deployment-pythonapi.yaml
kubectl apply -f infra/service-prediction.yaml
kubectl apply -f infra/service-redis.yaml

kubectl get pods -n w255
kubectl get svc -n w255

echo "7. Wait for your API to be accessible"
kubectl rollout status deployment/deployment-python-api -w

echo "8. Forwarding the local port to access the service endpoint"
kubectl port-forward -n w255 service/apps-deployment-service 8000:8000 &
PID=$!

echo "9. Wait for the /health endpoint to return a 200 and then move on"
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 1
    fi
done

echo "10. Test cases for different endpoints..."

echo "Test 1: testing '/hello' endpoint with ?name=Mamesa"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Mamesa"

echo "Test 2: testing '/hello' endpoint with ?name=John Luc Picard"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=John-Luc-Picard"

echo "Test 3: testing '/hello' endpoint with no input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?"

echo "Test 4: testing '/hello' endpoint with empty space"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=%20"

echo "Test 5: testing '/hello' endpoint with numeric input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=9821321"

echo "Test 6: testing '/hello' endpoint mamesa=name input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?mamesa=name"

echo "Test 7: testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "Test 8: testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

# echo "Test 16: testing '/openapi.json' endpoint and return json format text"
# curl -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

echo "Test 9: testing the health endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"

curl -s -w "%{http_code}\n" -X POST "http://localhost:8000/project-predict" -H "Content-Type: application/json" -d '{"text": ["example 1", "example 2"]}'

kill ${PID}

kubectl delete -f infra/deployment-pythonapi.yaml
kubectl delete -f infra/deployment-redis.yaml
kubectl delete -f infra/service-prediction.yaml
kubectl delete -f infra/service-redis.yaml

docker rmi -f my-api

minikube stop
minikube delete

# docker rmi $(docker images -f "reference=gcr.io/k8s-minikube/*" -q)

cd ..

