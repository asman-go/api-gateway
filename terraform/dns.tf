# Создание зоны DNS
# https://yandex.cloud/ru/docs/compute/tutorials/bind-domain-vm/terraform
resource "yandex_dns_zone" "domain-zone" {
  name        = "asman-domain-zone"
  description = "Asman domain zone"

  zone   = "${var.domain.domain-zone}."
  public = true

  provider = yandex.with-project-info
}

# Создание ресурсной записи типа А на наш instance
resource "yandex_dns_recordset" "record" {
  zone_id = yandex_dns_zone.domain-zone.id
  name    = "${local.domain}."
  type    = "A"
  ttl     = 600
  data    = ["${module.vm-instance.external_ip}"]

  provider = yandex.with-project-info
}
