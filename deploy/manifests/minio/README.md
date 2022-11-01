# MinIO

## Installation

```bash
helm template minio bitnami/minio --kube-version $CLUSTER_K8S_VERSION -n minio --output-dir ../ -f values.yaml --version 11.10.9
```

## Connect to MinIO server

### UI

```bash
kubectl port-forward svc/minio 9001:9001 -n minio
```

API:

```bash
kubectl port-forward svc/minio 9000:9000 -n minio
```

### MinIO client

```bash

# get minio credentials
export ROOT_USER=$(kubectl get secret -n minio minio -o jsonpath="{.data.root-user}" | base64 -d)
export ROOT_PASSWORD=$(kubectl get secret -n minio minio -o jsonpath="{.data.root-password}" | base64 -d)

# run with kubectl
kubectl run \
  -n minio \
  --rm \
  -it \
  # can't restart=Never, as it will need to wait for istio sidecar to be ready
  # --restart=Never \
  --image europe-docker.pkg.dev/pbl6-363916/mirror/minio-client:2022.10.29-debian-11-r0 \
  --env MINIO_SERVER_ROOT_USER=$ROOT_USER \
  --env MINIO_SERVER_ROOT_PASSWORD=$ROOT_PASSWORD \
  --env MINIO_SERVER_HOST=minio \
  minio-client -- admin info minio

# see result with
kubectl logs -n minio minio-client

# run with docker
kubectl port-forward svc/minio 9000:9000 -n minio

# for linux only
docker run \
  --rm \
  -it \
  --network host \
  --env MINIO_SERVER_ROOT_USER=$ROOT_USER \
  --env MINIO_SERVER_ROOT_PASSWORD=$ROOT_PASSWORD \
  --env MINIO_SERVER_HOST=localhost \
  bitnami/minio-client:2022.10.29-debian-11-r0 \
  admin info minio

```
