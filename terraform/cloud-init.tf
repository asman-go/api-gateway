locals {
  cert-fullchain-path = "/etc/certs/fullchain.pem"
  cert-privkey-path   = "/etc/certs/privkey.pem"
}

locals {
  cloud-init-yaml = yamlencode(
    {
      # User setup configuration
      "ssh_pwauth" : "no",
      "users" : [{
        "name" : local.default-user,
        "sudo" : "ALL=(ALL) NOPASSWD:ALL",
        "shell" : "/bin/bash",
        "ssh_authorized_keys" : [
          file("${path.module}/ycvm.pub")
        ]
      }],
      # Commands to run at the end of the cloud-init process
      "runcmd" : [
        "echo 'Hello, World!' > /etc/hello-world.txt",
        "chmod 666 /var/run/docker.sock",
      ],
      "write_files" : [
        {
          "path" : local.cert-privkey-path,
          "content" : data.yandex_cm_certificate_content.certificate.private_key
        },
        {
          "path" : local.cert-fullchain-path,
          "content" : join("\n", data.yandex_cm_certificate_content.certificate.certificates)
        },
        {
          # Задаем пароль при инициализации базы
          "path" : "/etc/init.sql",
          "content" : templatefile("${path.module}/configs/postgres/init.sql", {
            POSTGRES_USER     = var.postgres-secrets.user
            POSTGRES_PASSWORD = var.postgres-secrets.password
          })
        },
        {
          "path" : "/etc/nginx.default.conf",
          "content" : templatefile("${path.module}/configs/nginx/nginx.default.conf", {
            DOMAIN        = local.domain
            GW_LOCAL_HOST = var.gateway-config.local-host
            GW_LOCAL_PORT = var.gateway-config.local-port
          }),
        },
        {
          "path" : "/etc/fluentbit/fluentbit.conf",
          "content" : templatefile("${path.module}/configs/fluentbit/fluentbit.conf", {
            FLUENT_BIT_HOST = "fluentbit"
            FLUENT_BIT_PORT = 24224
            YC_GROUP_ID     = yandex_logging_group.group.id
          }),
        },
        {
          "path" : "/etc/fluentbit/parsers.conf",
          "content" : file("${path.module}/configs/fluentbit/parsers.conf")
        }
      ],
    }
  )
}

data "cloudinit_config" "cloud-init" {
  gzip          = false
  base64_encode = false

  part {
    filename     = "cloud-config.yaml"
    content_type = "text/cloud-config"

    content = local.cloud-init-yaml
  }
}
