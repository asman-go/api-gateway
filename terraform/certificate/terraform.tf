terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
    local = {
      source = "hashicorp/local"
    }
  }
  required_version = ">= 0.13"
}

data "yandex_resourcemanager_cloud" "cloud" {
  name = var.cloud-name
}

data "yandex_resourcemanager_folder" "folder" {
  cloud_id = data.yandex_resourcemanager_cloud.cloud.id
  name     = var.folder-name
}

provider "yandex" {
  alias     = "with-project-info"
  cloud_id  = data.yandex_resourcemanager_cloud.cloud.id
  folder_id = data.yandex_resourcemanager_folder.folder.id
}
