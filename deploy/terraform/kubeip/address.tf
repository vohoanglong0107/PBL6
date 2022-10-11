resource "google_compute_address" "kubeip_address" {
  // labels only support in beta
  provider = google-beta
  name     = "kubeip-ip"
  project  = var.project_id
  // kubeip query this label to find the address
  labels = {
    kubeip = var.cluster_name
  }
}
