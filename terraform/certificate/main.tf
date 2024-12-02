
# https://yandex.cloud/ru/docs/dns/operations/zone-create-public
data "yandex_dns_zone" "domain-zone" {
  name = var.domain-zone-name

  provider = yandex.with-project-info
}

# https://yandex.cloud/ru/docs/certificate-manager/tf-ref
resource "yandex_cm_certificate" "cert-domain" {
  name    = "cert-domain"
  domains = [var.domain]

  managed {
    challenge_type  = "DNS_CNAME"
    challenge_count = 1 # "example.com" and "*.example.com" has the same DNS_CNAME challenge
  }

  provider = yandex.with-project-info
}

# Прописываем DNS запись для прохождения челленджа
resource "yandex_dns_recordset" "validation-record" {
  count   = yandex_cm_certificate.cert-domain.managed[0].challenge_count
  zone_id = data.yandex_dns_zone.domain-zone.id
  name    = yandex_cm_certificate.cert-domain.challenges[count.index].dns_name
  type    = yandex_cm_certificate.cert-domain.challenges[count.index].dns_type
  data    = [yandex_cm_certificate.cert-domain.challenges[count.index].dns_value]
  ttl     = 600

  provider = yandex.with-project-info
}

data "yandex_cm_certificate" "cert-domain" {
  depends_on      = [yandex_dns_recordset.validation-record]
  certificate_id  = yandex_cm_certificate.cert-domain.id
  wait_validation = true

  provider = yandex.with-project-info
}

data "yandex_cm_certificate_content" "cert-domain-content" {
  depends_on      = [data.yandex_cm_certificate.cert-domain]
  certificate_id  = yandex_cm_certificate.cert-domain.id
  wait_validation = true

  provider = yandex.with-project-info
}
