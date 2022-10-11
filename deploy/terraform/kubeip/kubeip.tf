// https://github.com/doitintl/kubeip

resource "kubernetes_config_map" "kubeip" {
  metadata {
    name      = "kubeip-config"
    namespace = "kube-system"
    labels = {
      app = "kubeip"
    }
  }

  data = {
    KUBEIP_LABELKEY            = "kubeip"
    KUBEIP_LABELVALUE          = var.cluster_name
    KUBEIP_NODEPOOL            = var.ingress_pool
    KUBEIP_FORCEASSIGNMENT     = "true"
    KUBEIP_ADDITIONALNODEPOOLS = ""
    KUBEIP_TICKER              = "5"
    KUBEIP_ALLNODEPOOLS        = "false"
    KUBEIP_ORDERBYLABELKEY     = "priority"
    KUBEIP_ORDERBYDESC         = "true"
    KUBEIP_COPYLABELS          = "false"
    KUBEIP_CLEARLABELS         = "false"
    KUBEIP_DRYRUN              = "false"
  }
}

resource "kubernetes_deployment" "kubeip" {
  metadata {
    name      = "kubeip"
    namespace = "kube-system"
    labels = {
      app = "kubeip"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "kubeip"
      }
    }

    template {
      metadata {
        labels = {
          app = "kubeip"
        }
      }

      spec {
        priority_class_name = "system-cluster-critical"
        node_selector = {
          "cloud.google.com/gke-nodepool" = var.node_pool
        }
        container {
          name              = "kubeip"
          image             = "doitintl/kubeip:latest"
          image_pull_policy = "Always"

          env {
            name = "KUBEIP_LABELKEY"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_LABELKEY"
              }
            }
          }

          env {
            name = "KUBEIP_LABELVALUE"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_LABELVALUE"
              }
            }
          }

          env {
            name = "KUBEIP_NODEPOOL"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_NODEPOOL"
              }
            }
          }

          env {
            name = "KUBEIP_FORCEASSIGNMENT"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_FORCEASSIGNMENT"
              }
            }
          }

          env {
            name = "KUBEIP_ADDITIONALNODEPOOLS"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_ADDITIONALNODEPOOLS"
              }
            }
          }

          env {
            name = "KUBEIP_TICKER"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_TICKER"
              }
            }
          }

          env {
            name = "KUBEIP_ALLNODEPOOLS"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_ALLNODEPOOLS"
              }
            }
          }

          env {
            name = "KUBEIP_ORDERBYLABELKEY"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_ORDERBYLABELKEY"
              }
            }
          }

          env {
            name = "KUBEIP_ORDERBYDESC"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_ORDERBYDESC"
              }
            }
          }

          env {
            name = "KUBEIP_COPYLABELS"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_COPYLABELS"
              }
            }
          }

          env {
            name = "KUBEIP_CLEARLABELS"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_CLEARLABELS"
              }
            }
          }

          env {
            name = "KUBEIP_DRYRUN"
            value_from {
              config_map_key_ref {
                name = kubernetes_config_map.kubeip.metadata.0.name
                key  = "KUBEIP_DRYRUN"
              }
            }
          }

          resources {
            limits = {
              cpu    = "50"
              memory = "50Mi"
            }
            requests = {
              cpu    = "50m"
              memory = "50Mi"
            }
          }
        }
        restart_policy       = "Always"
        service_account_name = kubernetes_service_account.kubeip.metadata.0.name
      }
    }
  }

  timeouts {
    create = "3m"
    update = "3m"
    delete = "3m"
  }
}

resource "kubernetes_cluster_role" "kubeip" {
  metadata {
    name = "kubeip"
  }

  rule {
    api_groups = [""]
    resources  = ["pods"]
    verbs      = ["get", "list", "watch"]
  }

  rule {
    api_groups = [""]
    resources  = ["nodes"]
    verbs      = ["get", "list", "watch", "patch"]
  }
}

resource "kubernetes_cluster_role_binding" "kubeip" {
  metadata {
    name = "kubeip"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.kubeip.metadata.0.name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.kubeip.metadata.0.name
    namespace = "kube-system"
  }
}
