terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.38.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.38.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.13.1"
    }
  }

  required_version = ">= 1.3.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Configure kubernetes provider with Oauth2 access token.
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/client_config
# This fetches a new token, which will expire in 1 hour.
data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}
module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "~> 5.0"

  project_id   = var.project_id
  network_name = local.vpc_name

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
        ip_cidr_range = "192.168.24.0/21"
      },
      {
        range_name    = local.services_ip_range_name
        ip_cidr_range = "192.168.32.0/21"
      }
    ]
  }

  firewall_rules = [
    {
      name        = "http-nodeport"
      direction   = "INGRESS"
      description = "Allow http nodeport traffic for nginx ingress controller"
      allow = [
        {
          ports    = ["80"]
          protocol = "tcp"
        }
      ]
      ranges = ["0.0.0.0/0"]
    },
    {
      name        = "https-nodeport"
      direction   = "INGRESS"
      description = "Allow https nodeport traffic for nginx ingress controller"
      allow = [
        {
          ports    = ["443"]
          protocol = "tcp"
        }
      ]
      ranges = ["0.0.0.0/0"]
    },
    {
      name        = "ssh-nodeport"
      direction   = "INGRESS"
      description = "Allow ssh nodeport traffic for debugging"
      allow = [
        {
          ports    = ["22"]
          protocol = "tcp"
        }
      ]
      ranges = ["0.0.0.0/0"]
    }
  ]
}

module "gke" {
  source             = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  version            = "~> 23.1.0"
  kubernetes_version = "1.22.12-gke.1200"
  release_channel    = "STABLE"
  project_id         = var.project_id
  name               = local.gke_cluster_name
  regional           = false
  zones              = [var.zone]

  network                = module.vpc.network_name
  subnetwork             = module.vpc.subnets_names[0]
  ip_range_pods          = local.pods_ip_range_name
  ip_range_services      = local.services_ip_range_name
  create_service_account = true

  add_cluster_firewall_rules = false
  http_load_balancing        = false
  enable_private_nodes       = true

  remove_default_node_pool = true

  node_pools = [
    {
      name         = local.ingress_pool_name
      machine_type = "e2-micro"
      disk_size_gb = 10
      autoscaling  = false
      node_count   = 1
      auto_upgrade = true
      spot         = true
    },
    {
      name         = local.workers_pool_name
      machine_type = var.gke_node_machine_type
      disk_size_gb = var.gke_node_disk_size
      autoscaling  = false
      node_count   = var.gke_num_nodes
      auto_upgrade = true
      spot         = true
    }
  ]

  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/service.management",
      "https://www.googleapis.com/auth/trace.append",
    ]
  }

  node_pools_taints = {
    all = []
    "${local.ingress_pool_name}" = [
      {
        key    = "dedicated"
        value  = "ingress"
        effect = "NO_SCHEDULE"
      }
    ]
  }

  node_pools_tags = {
    "${local.ingress_pool_name}" = ["${local.ingress_pool_name}-node"]
    "${local.workers_pool_name}" = ["${local.workers_pool_name}-node"]
  }

  master_authorized_networks = [
    {
      cidr_block   = "0.0.0.0/0"
      display_name = "Anyone"
    }
  ]
}

module "kubeip" {
  source       = "./kubeip"
  node_pool    = local.workers_pool_name
  ingress_pool = local.ingress_pool_name
  cluster_name = local.gke_cluster_name
  project_id   = var.project_id
}

module "k8s-config" {
  source       = "./k8s-config"
  ingress_pool = local.ingress_pool_name
  depends_on = [
    module.kubeip
  ]
}
