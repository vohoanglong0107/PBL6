resource "kubernetes_config_map" "nginx" {
  metadata {
    name = "ingress-nginx-config"
  }
  data = {
    "nginx.conf" = file("${path.module}/nginx.conf")
  }
}

resource "kubernetes_deployment" "nginx" {
  metadata {
    name = "ingress-nginx"
    labels = {
      app = "IngressNginx"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "IngressNginx"
      }
    }
    template {
      metadata {
        labels = {
          app = "IngressNginx"
        }
      }
      spec {
        host_network = true
        dns_policy   = "ClusterFirstWithHostNet"
        node_selector = {
          "cloud.google.com/gke-nodepool" = var.ingress_pool
        }
        toleration {
          key    = "dedicated"
          value  = "ingress"
          effect = "NoSchedule"
        }

        container {
          image = "mirror.gcr.io/library/nginx"
          name  = "ingress-nginx"

          port {
            container_port = 80
            name           = "http"
            host_port      = 80
          }

          volume_mount {
            name       = "nginx-config"
            mount_path = "/etc/nginx/conf.d/default.conf"
            sub_path   = "nginx.conf"
            read_only  = true
          }

          resources {
            limits = {
              cpu    = "250m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "125m"
              memory = "50Mi"
            }
          }
        }
        volume {
          name = "nginx-config"
          config_map {
            name = kubernetes_config_map.nginx.metadata.0.name
          }
        }
      }
    }
  }
  timeouts {
    create = "1m"
    update = "1m"
    delete = "1m"
  }
}
