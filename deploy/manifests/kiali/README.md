# Kiali

## Update

```bash
helm template kiali-operator kiali/kiali-operator \
  --include-crds \
  --kube-version $CLUSTER_K8S_VERSION -n kiali-operator \
  --output-dir ./ -f kiali-operator/values.yaml --version 1.54.0
```

## Installation

```bash
k apply -k kiali-operator
k apply -f kiali-cr.yaml
```

It must be installed separately, else when deleting, the crds etc is gonna be deleted first, leaving the kiali-cr hang
