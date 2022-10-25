# MinIO

## Installation

```bash
helm template minio bitnami/minio --kube-version $CLUSTER_K8S_VERSION -n minio --output-dir ../ -f values.yaml --version 11.10.9
```
