output "kubeip_external_ip" {
  value       = module.kubeip.google_compute_address
  description = "KubeIP external IP"
}

output "cluster_location" {
  value       = module.gke.location
  description = "GKE cluster location"
}

output "cluster_type" {
  value       = module.gke.type
  description = "GKE cluster type"
}

output "cluster_zones" {
  value       = module.gke.zones
  description = "GKE cluster zones"
}

output "cluster_service_account" {
  value       = module.gke.service_account
  description = "GKE cluster service account"
}
