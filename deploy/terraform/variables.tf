variable "project_id" {
  description = "project id"
  type        = string
}

variable "region" {
  description = "region"
  type        = string
}

variable "zone" {
  description = "zone"
  type        = string
}

variable "gke_num_nodes" {
  default     = 3
  description = "number of gke nodes"
  type        = number
}

variable "gke_node_machine_type" {
  default     = "e2-medium"
  description = "gke node machine type"
  type        = string
}

variable "gke_node_disk_size" {
  default     = 100
  description = "gke node disk size in GB"
  type        = number
}

locals {
  gke_cluster_name       = "${var.project_id}-gke"
  vpc_name               = "${var.project_id}-vpc"
  subnet_name            = "${var.project_id}-subnet"
  pods_ip_range_name     = "${var.project_id}-pods-ip-range"
  services_ip_range_name = "${var.project_id}-services-ip-range"
  ingress_pool_name      = "${var.project_id}-ingress-pool"
  workers_pool_name      = "${var.project_id}-workers-pool"
}
