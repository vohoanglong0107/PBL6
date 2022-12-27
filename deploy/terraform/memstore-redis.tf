module "memorystore" {
  source  = "terraform-google-modules/memorystore/google"
  version = "6.0.0"

  name = "redis"

  project            = var.project_id
  region             = var.region
  location_id        = var.zone
  enable_apis        = true
  authorized_network = module.vpc.network_name
  memory_size_gb     = 1
}

output "redis_host" {
  value = module.memorystore.host
}

output "redis_port" {
  value = module.memorystore.port
}
