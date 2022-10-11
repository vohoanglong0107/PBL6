# Budget Load Balancer

## Install Helm

```bash
cd /tmp
wget https://get.helm.sh/helm-v3.10.0-linux-amd64.tar.gz
tar -zxvf helm-v3.10.0-linux-amd64.tar.gz
mv linux-amd64/helm ~/bin/helm # or any where included in $PATH
```

---
**Note**:
For this warning with gcp:

```bash
WARNING: the gcp auth plugin is deprecated in v1.22+, unavailable in v1.26+; use gcloud instead
```

Do this:

```bash
USE_GKE_GCLOUD_AUTH_PLUGIN=True gcloud container clusters get-credentials <cluster-name>
```

Be sure to install the auth plugin first:

```bash
gcloud components install gke-gcloud-auth-plugin
```

([this](https://github.com/helm/helm/issues/11069))
---

## Install Ingress Nginx Controller

```bash
helm upgrade ingress-nginx ingress-nginx \
    --install \
    --repo https://kubernetes.github.io/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --values values.yaml \
    --wait
```
