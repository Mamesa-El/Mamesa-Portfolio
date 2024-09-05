az acr login --name w255mids

TAG=$(git rev-parse --short HEAD)

IMAGE_PREFIX=$(az account list --all | jq '.[].user.name' | grep -i berkeley.edu | awk -F@ '{print $1}' | tr -d '"' | tr -d "." | tr '[:upper:]' '[:lower:]' | tr '_' '-' | uniq)
IMAGE_NAME=project
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"

sed "s/\[TAG\]/${TAG}/g" .k8s/overlays/prod/patch-deployment-project_copy.yaml > .k8s/overlays/prod/patch-deployment-project.yaml

docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .
docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_FQDN}:${TAG}
docker push ${IMAGE_FQDN}:${TAG}