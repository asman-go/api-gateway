data "yandex_compute_image" "container-optimized-image" {
  family = "container-optimized-image"
}

data "yandex_vpc_subnet" "subnet" {
  name = var.subnet-name
}

# Чтобы instance был доступен из сети
resource "yandex_vpc_address" "addr" {
  name = "instance-adress"
  external_ipv4_address {
    zone_id = var.zone
  }
}

resource "terraform_data" "postgres-password-hash" {
  input = var.postgres-password-hash
}

# Диск для данных PostgreSQL
resource "yandex_compute_disk" "postgres_data_disk" {
  name = "pg-data-disk"
  type = "network-hdd"
  zone = var.zone
  size = 10

  lifecycle {
    replace_triggered_by = [
      terraform_data.postgres-password-hash
    ]
  }
}

resource "yandex_compute_instance" "instance" {
  name = "api-gateway"

  platform_id = "standard-v3" # Intel Ice Lake, https://yandex.cloud/ru/docs/compute/concepts/vm-platforms
  zone        = var.zone

  service_account_id = var.sa-id
  resources {
    core_fraction = 50 # 50%
    cores         = 2
    memory        = 2
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.container-optimized-image.id
    }
  }

  secondary_disk {
    disk_id     = yandex_compute_disk.postgres_data_disk.id
    device_name = var.device-name
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.subnet.id
    # Управляем, какие порты открываем
    security_group_ids = [
      var.sg-id
    ]

    # Если хотим открыть наружу (дать публичный адрес)
    nat            = true
    nat_ip_address = yandex_vpc_address.addr.external_ipv4_address[0].address
  }

  metadata = {
    docker-compose = var.docker-compose
    user-data      = var.cloud-init
  }
}