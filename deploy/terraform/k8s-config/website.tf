// Sample website deployment to test the ingress

resource "kubernetes_service" "website" {
  metadata {
    name = "website"
    labels = {
      app = "website"
    }

  }
  spec {
    type = "ClusterIP"
    selector = {
      app = "website"
    }
    port {
      name        = "http"
      port        = 8080
      target_port = 80
    }
  }
}

resource "kubernetes_deployment" "website" {
  metadata {
    name = "website"
    labels = {
      app = "website"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "website"
      }
    }
    template {
      metadata {
        labels = {
          app = "website"
        }
      }
      spec {
        container {
          name  = "website"
          image = "mirror.gcr.io/library/nginx"
          port {
            container_port = 80
            name           = "http"
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
