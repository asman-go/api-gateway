variable "cloud-init" {
  description = "cloud-init config"
  type        = string
}

variable "docker-compose" {
  description = "Docker compose config"
  type        = string
}

variable "disk-name" {
  description = "Postgres disk name"
  type        = string
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