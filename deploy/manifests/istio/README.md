# Istio installation

## Helm template

```bash
CLUSTER_K8S_VERSION=$(kubectl version --short | grep Server | awk '{print $3}')
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo upate

# the -n flag is used here to select the istio-system namespace to provision and preprovision the config map (they got injected and kustomize doesn't know about it)
helm template istio-base --include-crds --kube-version $CLUSTER_K8S_VERSION -n istio-system > istio-base/helm-template.yaml

helm template istiod --include-crds --kube-version $CLUSTER_K8S_VERSION -n istio-system > istiod/helm-template.yaml

helm template istio-egress istio/gateway  --include-crds --kube-version $CLUSTER_K8S_VERSION -n istio-egress --output-dir istio-egress -f istio-egress/values.yaml

helm template istio-ingress --include-crds --kube-version $CLUSTER_K8S_VERSION -n istio-ingress > istio-ingress/helm-template.yaml
```

## Kustomize install

```bash
kubectl apply -k istio-base
kubectl apply -k istiod
kubectl apply -k istio-egress
# after installing cert-manager
kubectl apply -k istio-ingress
```
