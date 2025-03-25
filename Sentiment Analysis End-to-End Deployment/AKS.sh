# 1. log into azure
az login --tenant berkeleydatasciw255.onmicrosoft.com
# 2. Set subscription id using the ID given from class
az account set --subscription="0257ef73-2cbf-424a-af32-f3d41524e705"
# 3. Authenticate to the AKS cluster
az aks get-credentials --name w255-aks --resource-group w255 --overwrite-existing
# Configure workspace
kubectl config use-context w255-aks
# AKS login
az acr login --name w255mids
# 4. Get Name prefix from email address
export PREFIX=$(az account show | jq ".user.name" |  awk -F@ '{print $1}' | tr -d "\"" | tr -d "." | tr '[:upper:]' '[:lower:]')
# 5. Print out the prefix name
echo $PREFIX
# 6. Install kubelogin using brew command
# brew install Azure/kubelogin/kubelogin

echo "Testing tempt pods deployment"
# 7. Deploy a temp nginx container in your namespace
kubectl run nginx-dev --image=mcr.microsoft.com/oss/nginx/nginx:1.15.5-alpine --namespace $PREFIX
# 8. Check the temp container status
kubectl get pods --namespace $PREFIX
# 9. Delete the temp container
kubectl delete --all pods --namespace=$PREFIX
# 10. Tests for access in the default namespace which you should not have
kubectl run nginx-dev --image=mcr.microsoft.com/oss/nginx/nginx:1.15.5-alpine --namespace default

kubectl config set-context --current --namespace=mamesael

kubectl kustomize .k8s/overlays/prod
kubectl apply -k .k8s/overlays/prod

# kubectl get pods
# kubectl get svc
# kubectl get hpa
# kubectl logs $pod -c $init_container
# kubectl describe pod $pod

curl -o /dev/null -s -w "%{http_code}\n" -X GET "https://mamesael.mids255.com/health"

curl -s -w "%{http_code}\n" -X POST "https://mamesael.mids255.com/project-predict" -H "Content-Type: application/json" -d '{"text": ["example 1", "example 2"]}'

curl -s -w "%{http_code}\n" -X POST "https://mamesael.mids255.com/project-predict" -H "Content-Type: application/json" -d '{"text": ["🙂", "👍", "💡", "📚"]}'

# IMAGE_PREFIX=mamesael
kubectl delete --all deployments -n ${IMAGE_PREFIX}
kubectl delete --all services -n ${IMAGE_PREFIX}
kubectl delete --all virtualservices -n ${IMAGE_PREFIX}
kubectl delete --all horizontalpodautoscalers -n ${IMAGE_PREFIX}
kubectl delete --all configmaps -n ${IMAGE_PREFIX}
