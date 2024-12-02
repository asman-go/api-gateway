locals {
  default-user = "yc-user"
  # Нужно для правильного названия облачного диска postgres
  device-name        = "pgdata"
  logging-group-name = "gateway-logs"
}

# IAM

resource "yandex_iam_service_account" "sa-image-puller" {
  name        = "sa-image-puller"
  description = "Сервисный аккаунт для загрузки контейнеров из docker registry"

  provider = yandex.with-project-info
}

resource "yandex_resourcemanager_folder_iam_binding" "image-puller" {
  folder_id = data.yandex_resourcemanager_folder.folder.id
  role      = "container-registry.images.puller"
  members   = ["serviceAccount:${yandex_iam_service_account.sa-image-puller.id}"]

  provider = yandex.with-project-info
}

resource "yandex_resourcemanager_folder_iam_binding" "logging-writer" {
  folder_id = data.yandex_resourcemanager_folder.folder.id
  role      = "logging.writer"
  members   = ["serviceAccount:${yandex_iam_service_account.sa-image-puller.id}"]

  provider = yandex.with-project-info
}

resource "yandex_resourcemanager_folder_iam_binding" "certificate-downloader" {
  folder_id = data.yandex_resourcemanager_folder.folder.id
  role      = "certificate-manager.certificates.downloader"
  members   = ["serviceAccount:${yandex_iam_service_account.sa-image-puller.id}"]

  provider = yandex.with-project-info
}

# Logging

resource "yandex_logging_group" "group" {
  name             = local.logging-group-name
  retention_period = "168h" # 7d

  provider = yandex.with-project-info
}

# Certificate

data "yandex_cm_certificate" "certificate" {
  name            = "cert-domain"
  wait_validation = true

  provider = yandex.with-project-info
}

data "yandex_cm_certificate_content" "certificate" {
  depends_on = [data.yandex_cm_certificate.certificate]

  certificate_id  = data.yandex_cm_certificate.certificate.id
  wait_validation = true

  provider = yandex.with-project-info
}

# VM with docker compose

module "vm-instance" {
  source = "./vm-instance"

  cloud-init = data.cloudinit_config.cloud-init.rendered

  docker-compose = templatefile("${path.module}/configs/tpl.docker-compose.yaml", {
    DEFAULT_USER = local.default-user
    DEVICE_NAME  = local.device-name
    YC_GROUP_ID  = yandex_logging_group.group.id

    ASMAN_API_GATEWAY_IMAGE = var.gateway-docker-image

    GW_LOCAL_HOST = var.gateway-config.local-host
    GW_LOCAL_PORT = var.gateway-config.local-port

    ASMAN_ENVIRONMENT = var.gateway-config.environment

    USER_API_KEY  = var.api-keys.user-api-key
    ADMIN_API_KEY = var.api-keys.admin-api-key

    FACEBOOK_CLIENT_ID                  = var.facebook.client-id
    FACEBOOK_CLIENT_SECRET              = var.facebook.client-secret
    FACEBOOK_WEBHOOK_VERIFICATION_TOKEN = var.facebook.webhook-verification-token

    POSTGRES_LOCAL_HOST  = var.postgres-config.local-host
    POSTGRES_LOCAL_PORT  = var.postgres-config.local-port
    POSTGRES_REMOTE_PORT = var.postgres-config.remote-port
    POSTGRES_DB          = var.postgres-secrets.db
    POSTGRES_USER        = var.postgres-secrets.user
    POSTGRES_PASSWORD    = var.postgres-secrets.password

    FLUENT_BIT_HOST = "fluentbit"
    FLUENT_BIT_PORT = 24224

    CERT_FULLCHAIN_PATH = local.cert-fullchain-path
    CERT_PRIVKEY_PATH   = local.cert-privkey-path
  })

  sa-id       = yandex_iam_service_account.sa-image-puller.id
  sg-id       = yandex_vpc_security_group.instance-security-group.id
  subnet-name = yandex_vpc_subnet.asman-subnet-a.name
  zone        = var.zone
  disk-name   = local.device-name

  providers = {
    yandex = yandex.with-project-info
  }

  depends_on = [
    yandex_iam_service_account.sa-image-puller,
    yandex_vpc_subnet.asman-subnet-a,
    # module.certificate
  ]
}

