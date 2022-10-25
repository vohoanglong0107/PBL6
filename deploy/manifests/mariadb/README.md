# Mariadb

## Installation

```bash
# helm template do not remove, only add, so --output-dir ../ is safe here (does not remove values.yaml, kustomization.yaml, etc)
helm template mariadb bitnami/mariadb --kube-version $CLUSTER_K8S_VERSION -n mariadb --output-dir ../ -f values.yaml --version 11.3.3
```
