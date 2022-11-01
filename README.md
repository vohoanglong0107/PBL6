# PBL6

## Cluster Architecture

Following this [cheapest k8s cluster](https://redmaple.tech/blogs/affordable-kubernetes-for-personal-projects/) with terraform.

## Install cluster

Follow the install instructions in [deploy/manifests/README.md](deploy/manifests/README.md)

## Troubleshooting

### Error: Error creating NodePool

May becaused by too small ip range.
Check the ip range in both the subnet primary and secondary ranges.

```code
subnets = [
  {
    subnet_name           = local.subnet_name
    subnet_ip             = "10.186.0.0/20"
    subnet_region         = var.region
    subnet_private_access = true
  }
]

secondary_ranges = {
  "${local.subnet_name}" = [
    {
      range_name    = local.pods_ip_range_name
      ip_cidr_range = "192.168.24.0/21" # /24 for 256 ips, 110 pods or 1 node
    },
    {
      range_name    = local.services_ip_range_name
      ip_cidr_range = "192.168.32.0/21"
    }
  ]
}
```

(from [main.tf#L47](./deploy/terraform/main.tf#L47))

### Error: Error creating: Internal error occurred: failed calling webhook "admission-webhook-deployment...": failed to call webhook: Post "https://admission-webhook-service.kubeflow.svc:443/apply-poddefault?timeout=10s": dial tcp 192.168.25.10:4443: i/o timeout

Or something similar to this.

This is caused by the private GKE cluster internal firewall not allowing webhooks communication.
Check your firewall rules, kinda similar to this:

```code
// For webhooks
add_cluster_firewall_rules        = true
add_master_webhook_firewall_rules = true
// all webhooks ports, 4443 for kubeflow's admission-webhook-service
firewall_inbound_ports = ["4443", "8443", "9443", "15017"]
http_load_balancing    = false
enable_private_nodes   = true
```

(from [main.tf#L139](./deploy/terraform/main.tf#L139))

### Error: Internal error occurred: failed calling webhook "admission-webhook-deployment...": failed to call webhook: Post "https://admission-webhook-service.kubeflow.svc:443/apply-poddefault?timeout=10s": no endpoints available for service "admission-webhook-service"

Or some thing similar to this (no endpoints available).

This is caused by the admission-webhook-service not being ready. One of the reasons may be the private GKE cluster not allowing connect to the internet, so the webhook image cannot be pulled.

One possible soluton: Add Cloud NAT to the cluster.

```code
# Allow nodes to access the internet to pull images from other registries.
nats = [{
  name = "docker-gateway"
}]
```

(from [main.tf#L117](./deploy/terraform/main.tf#L117))
