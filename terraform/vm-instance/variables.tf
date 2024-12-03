variable "cloud-init" {
  description = "cloud-init config"
  type        = string
}

variable "docker-compose" {
  description = "Docker compose config"
  type        = string
}

variable "device-name" {
  description = "Postgres disk name: этот параметр для провязки диска в конфигурации и внутри контейнера / docker compose"
  type        = string
}

variable "postgres-password-hash" {
  # Сменили пароль — диск с данными пересоздаем?
  # Пока не знаю как лучше
  description = "Хеш пароля к Postgres"
  type        = string
  sensitive   = true
}

variable "sa-id" {
  description = "ID SA с ролью container-registry.images.puller"
  type        = string
}

variable "sg-id" {
  description = "Security Group ID"
  type        = string
}

variable "subnet-name" {
  description = "VPC subnet name"
  type        = string
}

variable "zone" {
  description = "DC zone"
  type        = string
}