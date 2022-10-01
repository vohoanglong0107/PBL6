# PBL6

## Cluster Architecture

Following this [cheapest k8s cluster](https://redmaple.tech/blogs/affordable-kubernetes-for-personal-projects/) with terraform. 

## Troubleshooting

### Error: Error creating NodePool
  May becaused by too small ip range.
  Check the ip range in both the subnet primary and secondary ranges.

  ```code
  subnets = [
    {
      subnet_name           = local.subnet_name
      subnet_ip             = "10.186.0.0/20"
      subnet_region         = var.region
      subnet_private_access = true
    }
  ]

  secondary_ranges = {
    "${local.subnet_name}" = [
      {
        range_name    = local.pods_ip_range_name
        ip_cidr_range = "192.168.24.0/21" # /24 for 256 ips, 110 pods or 1 node
      },
      {
        range_name    = local.services_ip_range_name
        ip_cidr_range = "192.168.32.0/21"
      }
    ]
  }
  ```