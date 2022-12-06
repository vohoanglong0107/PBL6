# Argo CD

## Login

When see the following, drop the https:// in front of the server URL

```bash
FATA[0000] dial tcp: address tcp///argocd.pbl6.mamlong34.monster/: unknown port
```

For example:

This does not work

```bash
argocd login https://argocd.pbl6.mamlong34.monster/
FATA[0000] dial tcp: address tcp///argocd.pbl6.mamlong34.monster: unknown port
```

This does work

```bash
argocd login argocd.pbl6.mamlong34.monster
```
