# Infra

## Init terraform

With remote state on GCS

```bash
terraform -chdir=deploy/terraform init -backend-config="bucket=<BUCKET_NAME>"
```

## Apply terraform

```bash
terraform -chdir=deploy/terraform apply
```

---
