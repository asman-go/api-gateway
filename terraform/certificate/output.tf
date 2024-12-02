output "cert_id" {
  description = "Certificate ID"
  value       = data.yandex_cm_certificate.cert-domain.id
}

output "chain" {
  value = join("\n", data.yandex_cm_certificate_content.cert-domain-content.certificates)
}

output "privkey" {
  value     = data.yandex_cm_certificate_content.cert-domain-content.private_key
  sensitive = true
}

data "local_file" "chain" {
  filename = "${path.module}/fullchain.pem"
  content  = join("\n", data.yandex_cm_certificate_content.cert-domain-content.certificates)
}

data "local_sensitive_file" "privkey" {
  filename = "${path.module}/privkey.pem"
  content  = data.yandex_cm_certificate_content.cert-domain-content.private_key
}
