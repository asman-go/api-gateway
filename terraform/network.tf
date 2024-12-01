# VPN Network

resource "yandex_vpc_network" "asman-network" {
  name        = "asman-network"
  description = "VPC network name"
  provider    = yandex.with-project-info
}

resource "yandex_vpc_subnet" "asman-subnet-a" {
  name           = "asman-subnet-a"
  network_id     = yandex_vpc_network.asman-network.id
  zone           = var.zone
  v4_cidr_blocks = ["10.5.0.0/24"]
  provider       = yandex.with-project-info
}

# Security group

resource "yandex_vpc_security_group" "instance-security-group" {
  # https://yandex.cloud/ru/docs/vpc/concepts/security-groups
  name       = "gateway-security-group"
  network_id = yandex_vpc_network.asman-network.id
  ingress {
    description    = "Allow SSH"
    protocol       = "ANY"
    port           = 22
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description    = "Allow HTTP"
    protocol       = "TCP"
    port           = 80
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description    = "Allow HTTPS"
    protocol       = "TCP"
    port           = 443
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description    = "Allow Postgres"
    protocol       = "TCP"
    port           = var.postgres-config.remote-port
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description    = "Permit ANY"
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  provider = yandex.with-project-info

  depends_on = [yandex_vpc_network.asman-network]
}
