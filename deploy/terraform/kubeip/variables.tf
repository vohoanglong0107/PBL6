variable "project_id" {
  type        = string
  description = "The project ID to deploy KubeIP to"
}

variable "cluster_name" {
  type        = string
  description = "The name of the GKE cluster to deploy KubeIP to"
}

variable "ingress_pool" {
  type        = string
  description = "The name of the node pool for the KubeIP to perform load balancing on"
}

variable "node_pool" {
  type        = string
  description = "The name of the node pool to deploy KubeIP to"
}
