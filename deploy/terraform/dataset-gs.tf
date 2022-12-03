module "dataset-gs" {
  source  = "terraform-google-modules/cloud-storage/google"
  version = "~> 3.4.0"

  names            = ["dataset"]
  prefix           = var.project_id
  randomize_suffix = true
  project_id       = var.project_id
  location         = var.region
}

output "dataset_bucket_url" {
  value       = module.dataset-gs.url
  description = "Dataset bucket name"
}

resource "google_service_account" "dataset" {
  account_id   = "dataset-service-account"
  display_name = "Dataset"
  project      = var.project_id
}

resource "google_project_iam_member" "dataset_viewer" {
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.dataset.account_id}@${var.project_id}.iam.gserviceaccount.com"
  project = var.project_id
}


resource "google_project_iam_member" "dataset_creator" {
  role    = "roles/storage.objectCreator"
  member  = "serviceAccount:${google_service_account.dataset.account_id}@${var.project_id}.iam.gserviceaccount.com"
  project = var.project_id
}


output "dataset_google_service_account" {
  value       = google_service_account.dataset.email
  description = "Dataset service account email"
}

resource "google_service_account_iam_member" "argo_executor" {
  service_account_id = google_service_account.dataset.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[ml/executor]"
}

resource "google_service_account_iam_member" "songs_uploader" {
  service_account_id = google_service_account.dataset.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[songs-uploader/songs-uploader]"
}
