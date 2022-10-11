# PBL6

## Cluster Architecture

Following this [cheapest k8s cluster](https://redmaple.tech/blogs/affordable-kubernetes-for-personal-projects/) with terraform.

## Installing Kubeflow on the cluster

### Prerequisites

Install Kustomize v3.2

  ```bash
  curl -sfL https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_linux_amd64 -o ~/bin/kustomize
  chmod +x ~/bin/kustomize
  ```

### Install

As Kubeflow is quite resource intensive, update the cluster node pool to have 3 nodes of n2-standard-2 (2 vCPUs, 8 GB memory).

To install Kubeflow on the cluster, run:
  
  ```bash
  deploy/scripts/install_kubeflow.sh
  ```

This will take a while.

Verify the installation by running:

  ```bash
  kubectl get pods -n cert-manager
  kubectl get pods -n istio-system
  kubectl get pods -n auth
  kubectl get pods -n knative-eventing
  kubectl get pods -n knative-serving
  kubectl get pods -n kubeflow
  kubectl get pods -n kubeflow-user-example-com
  ```

Connect to the Kubeflow dashboard by running:

  ```bash
  deploy/scripts/connect_to_kubeflow.sh
  ```

Then open <http://localhost:8080> in your browser. The default username is user@example.com and the password is 12341234.

### Upgrade

Install KPT

  ```bash
  curl -L https://github.com/GoogleContainerTools/kpt/releases/download/v1.0.0-beta.21/kpt_linux_amd64 -o ~/bin/kpt
  chmod +x ~/bin/kpt
  ```

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

### Error: Error creating: Internal error occurred: failed calling webhook "admission-webhook-deployment.kubeflow.org": failed to call webhook: Post "https://admission-webhook-service.kubeflow.svc:443/apply-poddefault?timeout=10s": dial tcp 192.168.25.10:4443: i/o timeout

Or something similar to this.

This is caused by the private GKE cluster internal firewall not allowing webhooks communication.
Check your firewall rules, kinda similar to this:
  
  ```code
  // For Kubeflow webhooks
  add_cluster_firewall_rules        = true
  add_master_webhook_firewall_rules = true
  // all webhooks ports, 4443 for kubeflow's admission-webhook-service
  firewall_inbound_ports = ["4443", "8443", "9443", "15017"]
  http_load_balancing    = false
  enable_private_nodes   = true
  ```

(from [main.tf#L139](./deploy/terraform/main.tf#L139))

### Error: Internal error occurred: failed calling webhook "admission-webhook-deployment.kubeflow.org": failed to call webhook: Post "https://admission-webhook-service.kubeflow.svc:443/apply-poddefault?timeout=10s": no endpoints available for service "admission-webhook-service"

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
