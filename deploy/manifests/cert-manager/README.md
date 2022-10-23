# Certmanager installation

## Helm template

```bash
helm template . --name-template cert-manager --include-crds --kube-version $CLUSTER_K8S_VERSION -n cert-manager > ./helm-template.yaml
```

## Kustomize install

```bash
kubectl apply -k .
```
