output "google_compute_address" {
  value       = google_compute_address.kubeip_address.address
  description = "The IP address of the KubeIP (load balancer)"
}
