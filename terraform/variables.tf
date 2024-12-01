variable "zone" {
  description = "В каком DC разместить сервис"
  type        = string
  default     = "ru-central1-a"
}

variable "domain" {
  description = "Информация о домене"
  type = object({
    domain-zone = string
    subdomain   = string
  })
  default = {
    domain-zone = "asman.ikemurami.com"
    subdomain   = "api"
  }
}

variable "gateway-docker-image" {
  description = "API Gateway Docker image"
  type        = string
}

variable "gateway-config" {
  description = "Переменные для нашего api-gateway"
  type = object({
    local-host  = string
    local-port  = number
    environment = string
  })
}

variable "api-keys" {
  description = "API Gateway keys"
  type = object({
    user-api-key  = string
    admin-api-key = string
  })
  sensitive = true
}

variable "facebook" {
  description = "Facebook API config"
  type = object({
    client-id                  = number
    client-secret              = string
    webhook-verification-token = string
  })
  sensitive = true
}

variable "postgres-config" {
  description = "Postgres Config"
  type = object({
    # Это имя контейнера, а не реальный хост!
    local-host = string
    # Вообще, это константа, на нее мы не влияем, но нам ее надо перекидывать
    local-port  = number
    remote-port = number
  })
}

variable "postgres-secrets" {
  description = "Postgres credentials"
  type = object({
    db       = string
    user     = string
    password = string
  })
  sensitive = true
}
