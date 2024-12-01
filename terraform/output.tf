output "external_domain" {
  value = "${var.domain.subdomain}.${var.domain.domain-zone}"
}

output "external_ip" {
  value = module.vm-instance.external_ip
}

output "ssh-connect" {
  value = "ssh -i ycvm ${local.default-user}@${var.domain.subdomain}.${var.domain.domain-zone}"
}
