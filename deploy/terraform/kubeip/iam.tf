// As Kubeib used k8s secrets to grant pods access,
// but in terraform it has been deprecated
// So workload identity is used instead
// https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#gcloud

resource "google_service_account" "kubeip" {
  account_id   = "kubeip-service-account"
  display_name = "kubeIP"
  project      = var.project_id
}

resource "google_project_iam_custom_role" "kubeip" {
  role_id     = "kubeip"
  title       = "kubeIP"
  description = "required permissions to run KubeIP"
  project     = var.project_id
  stage       = "GA"
  permissions = [
    "compute.addresses.list",
    "compute.instances.addAccessConfig",
    "compute.instances.deleteAccessConfig",
    "compute.instances.get",
    "compute.instances.list",
    "compute.projects.get",
    "container.clusters.get",
    "container.clusters.list",
    "resourcemanager.projects.get",
    "compute.networks.useExternalIp",
    "compute.subnetworks.useExternalIp",
    "compute.addresses.use",
  ]
}

resource "google_project_iam_member" "kubeip" {
  role    = google_project_iam_custom_role.kubeip.name
  member  = "serviceAccount:${google_service_account.kubeip.account_id}@${var.project_id}.iam.gserviceaccount.com"
  project = var.project_id
}

resource "kubernetes_service_account" "kubeip" {
  metadata {
    name      = "kubeip"
    namespace = "kube-system"
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.kubeip.email
    }
  }
  automount_service_account_token = true
}

resource "google_service_account_iam_member" "kubeip" {
  service_account_id = google_service_account.kubeip.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[kube-system/${kubernetes_service_account.kubeip.metadata.0.name}]"
}
